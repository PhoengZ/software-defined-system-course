# สถาปัตยกรรมสำหรับ Slide 4-5: www.chula.ac.th (Activity 8)
**วิชา:** 2110415 Software-Defined Systems  
**หัวข้อ:** Multi-Cloud Architecture for `www.chula.ac.th`

---

## 1. Mermaid Architecture Diagram

```mermaid
flowchart TD
    subgraph Users_Layer ["1. ผู้ใช้งาน (Global Public & Chula Community)"]
        User["ผู้ใช้งานทั่วไป / นิสิต / บุคลากร / ต่างชาติ"]
    end

    subgraph Edge_Routing ["2. Global Traffic Management & Multi-CDN Layer"]
        DNS["Global Anycast DNS & GSLB\n(AWS Route 53 / Cloudflare)"]
        WAF_CDN_A["Primary CDN & WAF\n(AWS CloudFront)"]
        WAF_CDN_B["Secondary CDN & WAF\n(Google Cloud CDN)"]
    end

    subgraph AWS_Cloud ["3. Primary Cloud Provider: AWS (Thailand Region)"]
        ALB_AWS["Application Load Balancer (ALB)"]
        ECS_AWS["Stateless WordPress Containers\n(AWS ECS / Fargate - Auto-scaling)"]
        Aurora_DB[("Amazon Aurora MySQL\n(Primary Read/Write)")]
        S3_AWS["Amazon S3 Bucket\n(Media Files & Uploads)"]
        Redis_AWS["Amazon ElastiCache (Redis)\n(Page/Object Cache)"]
    end

    subgraph GCP_Cloud ["4. Secondary / DR Cloud Provider: GCP (Thailand Region)"]
        ALB_GCP["Cloud Load Balancing"]
        GKE_GCP["Stateless WordPress Containers\n(Cloud Run / GKE - Standby/Auto-scaling)"]
        CloudSQL_DB[("Google Cloud SQL MySQL\n(Standby Read-Replica / DR)")]
        GCS_GCP["Google Cloud Storage (GCS)\n(Replicated Media Files)"]
    end

    %% User Flow
    User -->|"HTTPS Request"| DNS
    DNS -->|"Primary Traffic (e.g. 80-100%)"| WAF_CDN_A
    DNS -.->|"Failover / Overflow Traffic"| WAF_CDN_B

    %% CDN to Compute
    WAF_CDN_A -->|"Cache Miss / Dynamic Requests"| ALB_AWS
    WAF_CDN_B -->|"Cache Miss / Standby Route"| ALB_GCP

    %% AWS Internal
    ALB_AWS --> ECS_AWS
    ECS_AWS <--> Redis_AWS
    ECS_AWS --> Aurora_DB
    ECS_AWS <--> S3_AWS

    %% GCP Internal
    ALB_GCP --> GKE_GCP
    GKE_GCP --> CloudSQL_DB
    GKE_GCP <--> GCS_GCP

    %% Cross-Cloud Data Synchronization
    Aurora_DB -.->|"Asynchronous Cross-Cloud DB Replication"| CloudSQL_DB
    S3_AWS <-.->|"Automated Cross-Cloud Object Sync"| GCS_GCP
```

---

## 2. ข้อ 1: การออกแบบ Final Architecture (Multi-Cloud Pattern)

### ทำไมถึงเลือก "Multi-Cloud" แทน "Hybrid Cloud"?
1. **ธรรมชาติของระบบ (Public Read-Heavy Portal):**  
   `www.chula.ac.th` เป็นเว็บประชาสัมพันธ์และหน้าตาของมหาวิทยาลัย ข้อมูลทั้งหมดเป็นสาธารณะ (Public Data) ไม่มีความลับของข้อมูลนิสิตหรือข้อจำกัดด้าน PDPA ที่จำเป็นต้องเก็บกักไว้ใน Local On-Premise เหมือนระบบทะเบียน (`Reg Chula`)
2. **ความต้องการด้าน Uptime และ Disaster Recovery ระดับสูงสุด:**  
   หากเกิดภัยพิบัติหรือ Cloud เจ้าใดเจ้าหนึ่งล่มทั้ง Region ระบบจะสามารถ Failover ไปยัง Cloud อีกเจ้าได้ทันที ทำให้เว็บมหาวิทยาลัยมี Uptime 99.99%+ ตลอดเวลา
3. **กำจัดคอขวดของ On-premise อย่างสิ้นเชิง:**  
   ไม่ต้องพึ่งพาระบบเครือข่ายหรือห้องเซิร์ฟเวอร์ภายในมหาวิทยาลัย

### รายละเอียดการทำงานของแต่ละ Layer:
* **Layer 1: Global Routing & Multi-CDN Layer:**
  * ใช้ **Global Server Load Balancing (GSLB)** ตรวจเช็ค Health check ตลอดเวลา หากเกิดเหตุขัดข้องจะสลับ DNS ไปยังคลาวด์สำรองโดยอัตโนมัติ
  * แคชเนื้อหาข่าว สารสนเทศ รูปภาพ และไฟล์สถิติไว้ที่ Edge Servers ทั่วโลก ทราฟฟิกกว่า **90-95% จะถูกส่งจาก Edge ทันที** โดยไม่ต้องวิ่งเข้าเครื่องเซิร์ฟเวอร์
* **Layer 2: Compute Layer (Stateless Web Containers):**
  * สถาปัตยกรรม WordPress ถูกแยกให้เป็น **Stateless (ไร้สถานะ)** ทั้งหมด
  * รันบน Container (AWS Fargate และ GCP Cloud Run/GKE) พร้อมระบบ **Horizontal Pod Autoscaling (HPA)** ที่ยืดหดจำนวนเซิร์ฟเวอร์ได้อัตโนมัติตามโหลดผู้ใช้งาน
* **Layer 3: Storage Layer (Decoupled Assets):**
  * ไฟล์รูปภาพ ข่าวสาร และเอกสาร PDF (`wp-content/uploads`) ถูกแยกออกจากเซิร์ฟเวอร์ไปเก็บใน Object Storage (AWS S3) และซิงก์แบบสองทางไปยัง Google Cloud Storage (GCS)
* **Layer 4: Database Layer (Cross-Cloud DR):**
  * ใช้ Managed Relational Database (Amazon Aurora MySQL) เป็นโหนดหลัก (Active Read/Write) สำหรับแอดมินโพสต์ข่าว และทำ Async Replication ข้ามไปยัง Google Cloud SQL เป็นตัวสำรอง (Standby/DR)

---

## 3. ข้อ 2: การวิเคราะห์ข้อดีและข้อเสีย (Pros & Cons)

### ข้อดี (Pros):
1. **High Availability & Fault Tolerance สูงสุด (Zero Single Point of Failure):**  
   ไม่มีจุดล่มจุดเดียว หากระบบของ AWS ขัดข้อง ระบบจะสลับไปยัง GCP อัตโนมัติ เว็บมหาวิทยาลัยไม่มีวันดับ
2. **Near-Infinite Scalability (รองรับ Spike สบาย):**  
   เมื่อเกิดเหตุการณ์สำคัญระดับประเทศ (เช่น วันประกาศ TCAS, ข่าวด่วนมหาวิทยาลัย, งานพระราชทานปริญญาบัตร) Auto-scaling จะเพิ่มเครื่องรองรับผู้ใช้งานหลักแสนได้ภายในเวลาไม่กี่นาที
3. **Global Performance & Low Latency:**  
   ชาวต่างชาติ สถาบันจัดอันดับมหาวิทยาลัยโลก (QS / THE World University Rankings) หรือนิสิตต่างชาติเปิดดูเว็บได้เร็วเท่ากับคนในประเทศไทย เพราะข้อมูลถูกส่งจาก Edge CDN ที่อยู่ใกล้ที่สุด
4. **ป้องกันการโจมตีระดับ Terabits (DDoS Protection):**  
   Cloud WAF และ CDN ช่วยกรองบอทและการยิง DDoS ให้จบตั้งแต่ระดับ Edge โดยไม่กระทบเซิร์ฟเวอร์จริง
5. **No On-premise Hardware Maintenance:**  
   บุคลากรไอทีมหาวิทยาลัยไม่ต้องเสียเวลากับการเปลี่ยนอะไหล่ฮาร์ดดิสก์ แอร์ห้องเซิร์ฟเวอร์ดับ หรือระบบสำรองไฟสำรอง

### ข้อเสีย (Cons):
1. **Operational & Architectural Complexity:**  
   การดูแลระบบข้าม 2 Cloud ผู้ดูแลระบบต้องมีทักษะระดับสูง เช่น การเขียน Infrastructure as Code (Terraform), การจัดการ CI/CD และความเข้าใจคอนฟิกทั้ง AWS และ Google Cloud
2. **Cross-Cloud Data Transfer Cost (Egress Fee):**  
   มีค่าใช้จ่ายในการถ่ายโอนข้อมูลข้ามคลาวด์ โดยเฉพาะการ Replicate ข้อมูล Database และการ Sync สตอเรจมีเดียข้ามค่าย
3. **Data Consistency Latency:**  
   การจำลองฐานข้อมูลข้ามคลาวด์เป็นแบบ Asynchronous อาจมีความล่าช้าในการ Sync เล็กน้อย (เสี้ยววินาที) หากเกิด Failover กะทันหัน

---

## 4. ข้อ 3: Shortcomings ที่ยังคงเหลืออยู่เมื่อเทียบกับ On-Premise

สิ่งที่อาจารย์เน้นถามในโจทย์คือ **"แม้จะย้ายขึ้น Cloud สถาปัตยกรรมใหม่นี้ยังมีจุดด้อยอะไรเมื่อเทียบกับ On-premise ดั้งเดิม?"**:

1. **การเปลี่ยนรูปแบบต้นทุนจากคงที่เป็นแบบผันแปร (Opex vs Capex) & เสี่ยง Bill Shock:**  
   * *On-premise:* เป็นต้นทุนคงที่ (Capex) จ่ายค่าเซิร์ฟเวอร์ครั้งเดียว คำนวณงบประมาณรายปีของมหาวิทยาลัยได้แน่นอน  
   * *Multi-Cloud:* เป็นต้นทุนแปรผันตามการใช้งานจริง (Opex) หากเว็บถูกบอทสแครป หรือทีมงานคอนฟิก CDN Cache Policy ผิดพลาดจนรีเควสต์หลุดมาที่ Origin อาจทำให้งบประมาณคลาวด์พุ่งสูงเกินควบคุม
2. **การสูญเสียการควบคุมระดับกายภาพ (Loss of Low-Level Infrastructure Control):**  
   * มหาวิทยาลัยไม่สามารถเข้าถึงหรือควบคุม Hardware/Hypervisor ได้โดยตรง ต้องพึ่งพาข้อตกลงระดับบริการ (SLA) ของผู้ให้บริการคลาวด์ หากเกิดปัญหาเชิงลึกระดับคลาวด์ทำได้เพียงรอทาง Provider แก้ไข
3. **ต้องปรับทักษะของบุคลากรภายใน (Staff Reskilling):**  
   * บุคลากรฝ่ายไอทีของมหาวิทยาลัยที่คุ้นเคยกับการดูแล System Admin แบบ On-premise ดั้งเดิม ต้องปรับตัวและผ่านการเทรนทักษะด้าน Cloud Architecture และ Cloud Security อย่างหนัก

---

## 5. สรุปเนื้อหาสำหรับจัดใส่ Slide 4 และ Slide 5 (Presentation Ready)

### 📌 Slide 4: Final Architecture Design & Key Strategy
* **หัวข้อสไลด์:** Multi-Cloud Architecture for `www.chula.ac.th`
* **ภาพประกอบ:** แผนภาพ Mermaid Architecture Diagram ด้านบน
* **ประเด็นสำคัญที่จะพูด:**
  * **Strategy:** เลือกใช้ **Multi-Cloud (AWS + GCP)** เพราะเป็นเว็บประชาสัมพันธ์สาธารณะ ข้อมูลไม่มีชั้นความลับ (PDPA) มุ่งเน้น Uptime 99.99% และ Global Access
  * **Core Components:**
    * *Edge:* Multi-CDN (CloudFront + Cloud CDN) แคชเนื้อหาได้ >90%
    * *Compute:* Stateless WordPress Containers บน Container Service (Auto-scale ยืดหดได้ตามปริมาณข่าว)
    * *Storage & DB:* Decoupled S3/GCS Object Storage + Cross-Cloud DB Replication เพื่อทำ Disaster Recovery

---

### 📌 Slide 5: Evaluation (Pros, Cons & Shortcomings vs On-premise)
* **หัวข้อสไลด์:** Architectural Evaluation & Shortcomings
* **ตารางสรุป:**

| ด้าน | Multi-Cloud Architecture (ใหม่) | On-Premise เดิม |
| :--- | :--- | :--- |
| **Availability** | **99.99%+** (ทนทานต่อ Cloud Provider ล่มทั้งค่าย) | เสี่ยง Downtime สูง (Single Point of Failure ในศูนย์คอมฯ) |
| **Scalability** | **Auto-scale ในหลักนาที** รองรับ Traffic ข่าวด่วนได้มหาศาล | ขยายไม่ได้ มีขีดจำกัดตามจำนวนเซิร์ฟเวอร์ที่ซื้อไว้ |
| **Global Speed** | โหลดเร็วทั่วโลกด้วย Multi-CDN Edge Caching | โหลดช้าจากต่างประเทศเพราะวิ่งตรงเข้าไทย |

* **Remaining Shortcomings (จุดด้อยที่ยังเหลืออยู่เทียบกับ On-Premise):**
  1. **Cost Predictability:** เปลี่ยนเป็น Opex จ่ายตามจริง เสี่ยงงบประมาณบานปลายหากคอนฟิกพลาด ต่างจาก On-premise ที่งบประมาณนิ่ง
  2. **Operational Overhead:** ซับซ้อนกว่า On-premise ต้องใช้ความเชี่ยวชาญ Multi-Cloud DevOps (Terraform / CI/CD)
  3. **Loss of Control:** ต้องพึ่งพา SLA ของ Cloud ภายนอก ขาดการควบคุม Physical Infrastructure โดยสมบูรณ์
