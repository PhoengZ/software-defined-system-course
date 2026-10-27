# Assignment Solution: Activity 10 - Edge–Cloud Computing
**Course:** 2110415 Software-Defined System (2026/1)  
**Topic:** People Counting Service using Edge–Cloud Architecture  
**Student Name:** ________________________________________  
**Student ID:** __________________________________________  

---

## Part 1: mCV Attach Files (หลักฐานไฟล์ที่ต้องแนบส่ง)

### 1. Screenshot of AWS SageMaker AI (Jupyter Notebook)
> **คำแนะนำ:** แคปภาพหน้าต่าง Jupyter Notebook (`EndpointDeployment.ipynb`) ขณะรันเซลล์เสร็จสิ้นจนแสดงข้อความ `Endpoint Status = InService` หรือภาพหน้าจอ AWS SageMaker Endpoints Console ที่แสดงสถานะ InService

```markdown
<!-- วางรูปภาพที่นี่ (สามารถตั้งชื่อไฟล์เป็น sagemaker_notebook.png แล้ววางในโฟลเดอร์เดียวกัน) -->
![AWS SageMaker Jupyter Notebook](./sagemaker_notebook.png)
```

---

### 2. Screenshot of the "Welcome to People Counting Services" Webpage
> **คำแนะนำ:** แคปภาพหน้าจอของเว็บแอปพลิเคชันที่ URL `http://localhost:5173/` หลังจากสั่งรัน `docker compose up --build` สำเร็จ

```markdown
<!-- วางรูปภาพที่นี่ (สามารถตั้งชื่อไฟล์เป็น webpage_service.png แล้ววางในโฟลเดอร์เดียวกัน) -->
![Welcome to People Counting Services Webpage](./webpage_service.png)
```

---

### 3. Completed `People counting record sheet.xlsx`
> **คำแนะนำ:** ตรวจสอบว่าได้กรอกข้อมูลและบันทึกภาพลงในเซลล์ (`Insert -> Image -> Insert Image in Cell`) ครบทั้ง 10 รูป แล้วบันทึกไฟล์เป็นชื่อ `People counting record sheet.xlsx` เพื่อแนบส่งบน mCV

- [ ] บันทึกผลรูปที่ 1 - 4 (ภาพตัวอย่างที่กำหนดให้)
- [ ] บันทึกผลรูปที่ 5 - 10 (ภาพถ่ายในห้องเรียน พร้อม Ground Truth)
- [ ] คำนวณค่าเฉลี่ยในแถบ Result Summary ครบถ้วน
- [ ] ขนาดไฟล์ Excel ไม่เกิน 20 MB (ตามข้อกำหนดของ mCV)

---

## Part 2: ตารางสรุปผลการทดลอง (Result Summary Table)
> **คำแนะนำ:** นำค่าเฉลี่ยจากท้ายตาราง `People counting record sheet.xlsx` มากรอกลงในตารางด้านล่างนี้:

| Metric | Edge (YOLOv8n) | Cloud (YOLOv8x) | Edge–Cloud (Hybrid) |
| :--- | :---: | :---: | :---: |
| **Average Response Time (ms)** | `[กรอกค่า เช่น 120 ms]` | `[กรอกค่า เช่น 650 ms]` | `[กรอกค่า เช่น 280 ms]` |
| **Average Processing Time (ms)** | `[กรอกค่า เช่น 110 ms]` | `[กรอกค่า เช่น 85 ms]` | `[กรอกค่า เช่น 135 ms]` |
| **Average Accuracy (%)** | `[กรอกค่า เช่น 78.5%]` | `[กรอกค่า เช่น 95.0%]` | `[กรอกค่า เช่น 91.2%]` |

---

## Part 3: mCV Answer the Questions (คำตอบสำหรับ 3 คำถาม)

### Question 1: Performance Comparison
> **โจทย์:** In the result summary section (at the end of the record sheet), observe the values of Average Response Time (ms), Average Processing Time (ms), and Average Accuracy. Identify which setup (Edge, Cloud, or Edge–Cloud) shows highest or lowest values for each metric. Analyze the reasons behind these differences.

#### 1. สรุปค่าสูงสุด (Highest) และค่าต่ำสุด (Lowest) ของแต่ละ Metric:
- **Average Response Time (ms):**
  - **Highest:** `[ระบุ เช่น Cloud]` (ค่า: `______` ms)
  - **Lowest:** `[ระบุ เช่น Edge]` (ค่า: `______` ms)
- **Average Processing Time (ms):**
  - **Highest:** `[ระบุ เช่น Edge หรือ Edge-Cloud ขึ้นอยู่กับสเปกเครื่อง PC ของคุณ]` (ค่า: `______` ms)
  - **Lowest:** `[ระบุ เช่น Cloud]` (ค่า: `______` ms)
- **Average Accuracy (%):**
  - **Highest:** `[ระบุ เช่น Cloud]` (ค่า: `______` %)
  - **Lowest:** `[ระบุ เช่น Edge]` (ค่า: `______` %)

---

#### 2. บทวิเคราะห์สาเหตุเชิงเทคนิคเบื้องหลังความแตกต่าง (Detailed Analysis):
> **คำแนะนำ:** สามารถนำเนื้อหาเชิงเทคนิคด้านล่างนี้ไปปรับใช้หรือเสริมด้วยผลการทดลองจริงของคุณได้เลยครับ

1. **ด้าน Response Time (เวลาตอบสนองรวมที่ Client ได้รับ):**
   - **Edge มี Response Time ต่ำที่สุด:** เนื่องจากข้อมูลรูปภาพถูกประมวลผลอยู่บนเครื่อง Local Host โดยตรงผ่าน Local Loopback (`127.0.0.1`) ไม่ต้องส่งข้อมูลผ่านระบบเครือข่ายอินเทอร์เน็ต จึงไม่มี Network Latency และไม่มี Overhead จาก Round-Trip Time (RTT)
   - **Cloud มี Response Time สูงที่สุด:** เนื่องจาก Client ต้องส่งไฟล์รูปภาพขนาดเต็มผ่านอินเทอร์เน็ตขึ้นไปยัง AWS Cloud (Region Singapore: `ap-southeast-1`) แล้วรอให้ Cloud ประมวลผลก่อนส่งผลลัพธ์ JSON กลับมา ทำให้เกิด Transmission Latency + Propagation Delay ของระบบเครือข่ายเป็นปัจจัยหลัก
   - **Edge–Cloud (Hybrid) มี Response Time อยู่ในระดับปานกลาง:** หากผลการประเมินเบื้องต้นที่ Edge มี Confidence Score สูง ระบบจะส่งผลลัพธ์กลับทันที แต่หากโมเดลท้องถิ่นมีความไม่มั่นใจ (Confidence ต่ำ) จึงจะส่งต่อภาพไปยัง Cloud ทำให้ Response Time เฉลี่ยดีกว่าการส่งขึ้น Cloud ทุกครั้งอย่างมีนัยสำคัญ

2. **ด้าน Processing Time (เวลาที่โมเดลใช้ในการอนุมาน/Inference):**
   - **Cloud ประมวลผลได้รวดเร็วเมื่อเทียบกับขนาดโมเดล:** แม้โมเดล `YOLOv8x` จะมีขนาดพารามิเตอร์ที่ใหญ่มาก (~68.2M parameters) แต่ทำงานบนอินสแตนซ์ของ SageMaker ที่มีทรัพยากรการประมวลผลสูง จึงสามารถทำ Inference ได้อย่างมีประสิทธิภาพ
   - **Edge ใช้โมเดลขนาดเล็ก:** โมเดล `YOLOv8n` เป็นโมเดล Nano (~3.2M parameters) ที่ถูกออกแบบมาเพื่ออุปกรณ์ที่มีทรัพยากรจำกัด แม้จะรันบน CPU ท้องถิ่นก็สามารถประมวลผลได้อย่างรวดเร็ว
   - **Edge–Cloud Processing Time:** ในกรณีที่เกิดการส่งต่อ (Offload) ไปยัง Cloud เวลาการประมวลผลจะรวมทั้งขั้นตอนการคัดกรองเบื้องต้นที่ Edge และเวลาประมวลผลจริงบน Cloud

3. **ด้าน Accuracy (ความแม่นยำในการนับจำนวนคน):**
   - **Cloud มีความแม่นยำสูงสุด:** เนื่องจากใช้โมเดลขนาดใหญ่ `YOLOv8x` ซึ่งมีโครงสร้างเครือข่ายประสาทเทียมที่ลึก มีจำนวนพารามิเตอร์สูง และมีความละเอียดในการสกัดฟีเจอร์สูงมาก จึงสามารถตรวจจับคนที่ยืนซ้อนกัน (Occlusion), คนที่มีขนาดตัวเล็ก หรืออยู่ในสภาวะแสงไม่เหมาะสมได้อย่างแม่นยำ
   - **Edge มีความแม่นยำต่ำที่สุด:** โมเดล `YOLOv8n` ถูกบีบอัดให้มีน้ำหนักเบาเพื่อความเร็ว ทำให้สูญเสียความสามารถในการตรวจจับวัตถุขนาดเล็กหรือผู้คนที่ซ้อนทับกันหนาแน่น ส่งผลให้อัตราการตรวจจับตกหล่น (False Negative) มีมากกว่า
   - **Edge–Cloud รักษาความแม่นยำได้ใกล้เคียง Cloud:** เนื่องจากใช้กลไก Dynamic Offloading โดยนำรูปภาพที่ Edge ตรวจจับได้ไม่มั่นใจส่งต่อไปให้ Cloud ประมวลผลซ้ำ ทำให้ความแม่นยำโดยรวมสูงขึ้นใกล้เคียงกับการส่งทุกรูปไปที่ Cloud

---

### Question 2: Suitable Use Cases
> **โจทย์:** Based on the results, which characteristics, needs, or requirements are best suited for each setup (Edge/Cloud/Edge–Cloud), considering the accuracy, response time, and cost trade-offs?

#### 1. ตารางเปรียบเทียบ Trade-offs ของแต่ละสถาปัตยกรรม:

| Architecture | ข้อเด่น (Strengths) | ข้อจำกัด (Limitations) | ปัจจัยด้านต้นทุน (Cost Trade-offs) |
| :--- | :--- | :--- | :--- |
| **Edge Computing** | • Response Time ต่ำมาก (Real-time)<br>• ใช้งานได้แม้ไม่มีอินเทอร์เน็ต (Offline)<br>• ข้อมูลส่วนบุคคลไม่รั่วไหล (Privacy) | • ความแม่นยำจำกัดในฉากที่มีคนหนาแน่น<br>• ทรัพยากรเครื่องปลายทางต้องรองรับ | • ไม่มีค่าใช้จ่าย Cloud Server / API<br>• ลงทุนเฉพาะฮาร์ดแวร์ Edge Device ครั้งเดียว |
| **Cloud Computing** | • ความแม่นยำสูงที่สุด (YOLOv8x)<br>• Scale รองรับโหลดมหาศาลได้ง่าย<br>• ปรับเปลี่ยนโมเดลรวมศูนย์ได้ทันที | • Latency สูงจากเครือข่ายอินเทอร์เน็ต<br>• สิ้นเปลือง Bandwidth สูง<br>• ไม่สามารถทำงานได้หากเน็ตหลุด | • มีค่าใช้จ่าย Cloud Hosting/Inference ตลอดเวลา<br>• เสียค่า Data Transfer และค่า Endpoint รายชั่วโมง |
| **Edge–Cloud (Hybrid)** | • ได้ความแม่นยำสูงใกล้เคียง Cloud<br>• ประหยัด Bandwidth ได้มากกว่า Cloud ล้วน<br>• Latency เฉลี่ยดีกว่า Cloud | • ความซับซ้อนของระบบสูงขึ้น (Routing logic)<br>• ต้องบริหารจัดการทั้ง Edge และ Cloud | • ประหยัดค่า Cloud API ได้มาก (ส่งเฉพาะเคสยาก)<br>• จุดสมดุลของ Cost และ Performance ดีที่สุด |

---

#### 2. การวิเคราะห์ความเหมาะสมและการนำไปใช้งานจริง (Suitable Use Cases):

1. **Edge Computing เหมาะสำหรับ:**
   - **ลักษณะความต้องการ:** ต้องการการตอบสนองที่รวดเร็วระดับมิลลิวินาที (Ultra-low Latency), แบนด์วิดท์มีจำกัดหรืออยู่ในพื้นที่ห่างไกล, และข้อมูลมีความอ่อนไหวสูงด้าน Privacy (ไม่ต้องการส่งภาพผู้คนขึ้น Public Internet)
   - **ตัวอย่างการใช้งาน:**
     - ประตูเข้า-ออกอัตโนมัติ (Automated Turnstile / Gate Counter) ที่ต้องการสั่งเปิด-ปิดทันที
     - กล้องตรวจจับคนเดินข้ามถนนบริเวณทางม้าลายอัจฉริยะ (Smart Crosswalk)
     - โดรนกู้ภัยหรือกล้องวงจรปิดในพื้นที่ที่ไม่มีสัญญาณอินเทอร์เน็ต

2. **Cloud Computing เหมาะสำหรับ:**
   - **ลักษณะความต้องการ:** ต้องการความแม่นยำสูงสุดเป็นอันดับหนึ่ง (High Precision), การประมวลผลเป็นแบบรวมศูนย์ (Centralized Processing), หรือเป็นงานแบบ Batch Processing ที่ไม่จำกัดเวลาตอบสนองแบบ Real-time
   - **ตัวอย่างการใช้งาน:**
     - การนับจำนวนคนเพื่อสรุปสถิติผู้เข้าชมงานนิทรรศการหรือคอนเสิร์ตขนาดใหญ่ประจำวัน
     - การตรวจสอบความหนาแน่นของผู้โดยสารจากกล้องวงจรปิดทั่วทั้งสถานีรถไฟฟ้าเพื่อการวางแผนเชิงยุทธศาสตร์
     - ระบบตรวจสอบความปลอดภัยระดับสูงที่ต้องการความผิดพลาดต่ำที่สุด

3. **Edge–Cloud (Hybrid Computing) เหมาะสำหรับ:**
   - **ลักษณะความต้องการ:** ต้องการระบบที่มีความแม่นยำสูง แต่มีข้อจำกัดด้านงบประมาณค่าบริการ Cloud และปริมาณ Bandwidth ของระบบเครือข่าย
   - **ตัวอย่างการใช้งาน:**
     - ระบบ Smart Retail ในห้างสรรพสินค้า: จัดการนับลูกค้าทั่วไปที่เดินผ่านหน้าร้านแบบเร็วๆ ด้วย Edge แต่หากมีกลุ่มคนยืนบังกันหรือมีพฤติกรรมซับซ้อน จะส่งภาพขึ้นไปวิเคราะห์ต่อบน Cloud
     - กล้องเฝ้าระวังความปลอดภัยใน Smart City หรือมหาวิทยาลัย ที่มีกล้องหลายร้อยตัว การส่งภาพทุกตัวขึ้น Cloud ตลอดเวลาจะทำให้เครือข่ายล่ม จึงใช้ Edge คัดกรองและส่งเฉพาะภาพที่มีความไม่มั่นใจขึ้น Cloud

---

### Question 3: AWS Cleanup Confirmation
> **โจทย์:** Have you completed the cleanup step after finishing the assignment to avoid unexpected AWS charges?

#### รายการยืนยันการทำความสะอาดระบบ (Cleanup Checklist):
- [x] **Local Docker Containers:** ได้สั่งรันคำสั่ง `docker compose down` เพื่อหยุดและลบ Container ทั้งหมดในเครื่องเรียบร้อยแล้ว
- [x] **Amazon SageMaker Endpoint:** ได้รัน Code Cells ในส่วน Cleanup ของไฟล์ `EndpointDeployment.ipynb` เพื่อลบ Endpoint `YOLOv8` และ Endpoint Configuration เรียบร้อยแล้ว (ตรวจสอบในหน้า Console แล้วไม่พบ Endpoint หลงเหลืออยู่)
- [x] **Deployable Model:** ลบโมเดล `YOLOv8` ออกจากหน้า SageMaker Model Console เรียบร้อยแล้ว
- [x] **SageMaker Notebook Instance:** ได้ทำการ Stop และ Delete โน้ตบุ๊กอินสแตนซ์ `sds-edge-computing` เรียบร้อยแล้ว
- [x] **AWS IAM User & Access Keys:** ได้เข้าไปทำการ Deactivate และ Delete Access Key รวมถึงลบ IAM User `sds-sagemaker` เรียบร้อยแล้ว

#### ข้อความสำหรับคัดลอกไปตอบบนระบบ mCV:
```text
Yes, I have completed all the cleanup steps thoroughly to avoid any unexpected AWS charges:
1. Stopped and removed all local Docker containers using 'docker compose down'.
2. Executed the cleanup section in EndpointDeployment.ipynb, successfully deleting the SageMaker Endpoint (YOLOv8), Endpoint Configuration, and Model.
3. Stopped and deleted the SageMaker Notebook instance (sds-edge-computing).
4. Deactivated and deleted the IAM Access Key and the IAM User (sds-sagemaker).
5. Verified via AWS Management Console that no active endpoints or billable resources remain running.
```
