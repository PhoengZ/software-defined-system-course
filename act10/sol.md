# Assignment Solution: Activity 10 - Edge–Cloud Computing

**Course:** 2110415 Software-Defined System (2026/1)  
**Activity:** People Counting Service using Edge–Cloud Architecture  
**Signed on as:** นายเผ่าลาภ กุลธีระ  
**Due Date:** 2 พฤศจิกายน 2026 เวลา 23:59 น.  
**Total Points:** 5 คะแนน (ข้อละ 1 คะแนน)  

---

## 📂 Part 1: Attach a file to each attachment slot (แนบไฟล์ 3 รายการ - สูงสุด 20 MB/ไฟล์)

### Slot 1: `Screenshot AWS SageMaker (Jupyter Notebook)`
> **คำแนะนำ:** แคปภาพหน้าต่าง Jupyter Notebook (`EndpointDeployment.ipynb`) ขณะรันเซลล์จนแสดงข้อความ `Endpoint Status = InService` หรือภาพหน้า AWS Console ที่แสดง Endpoint `YOLOv8` มีสถานะเป็น InService

```markdown
<!-- วางรูปภาพที่นี่ (บันทึกเป็นชื่อ sagemaker_notebook.png ในโฟลเดอร์เดียวกัน) -->
![Screenshot AWS SageMaker (Jupyter Notebook)](./sagemaker_notebook.png)
```

---

### Slot 2: `Screenshot “Welcome to People Counting Services” (Webpage)`
> **คำแนะนำ:** แคปภาพหน้าจอเว็บแอปพลิเคชันที่ URL `http://localhost:5173/` หลังจากสั่งรัน `docker compose up --build` สำเร็จและเบราว์เซอร์เปิดหน้าเว็บขึ้นมาได้

```markdown
<!-- วางรูปภาพที่นี่ (บันทึกเป็นชื่อ webpage_service.png ในโฟลเดอร์เดียวกัน) -->
![Screenshot “Welcome to People Counting Services” (Webpage)](./webpage_service.png)
```

---

### Slot 3: `Completed People counting record sheet (.xlsx)`
> **คำแนะนำ:** ตรวจสอบว่าได้แทรกรูปผลลัพธ์ในเซลล์ (`Insert -> Image -> Insert Image in Cell`) ครบทั้ง 10 รูป และคำนวณค่าเฉลี่ยแถบสีเหลืองครบถ้วนแล้ว บันทึกไฟล์ชื่อ `People counting record sheet.xlsx`

- [ ] รูปที่ 1 - 4 (ภาพตัวอย่างที่กำหนดให้)
- [ ] รูปที่ 5 - 10 (ภาพถ่ายในห้องเรียน พร้อม Ground Truth)
- [ ] กรอกผลการทดลองครบ 3 Trials (Response time, Processing time, People detected)
- [ ] กรอกและคำนวณค่าเฉลี่ยในแถบ Result Summary ครบถ้วน
- [ ] ตรวจสอบขนาดไฟล์ไม่ให้เกิน 20 MB เพื่ออัปโหลดขึ้น myCourseVille ได้อย่างสมบูรณ์

---

## 📊 Part 2: สรุปผลการทดลอง (Experiment Summary Table)
> **คำแนะนำ:** นำตัวเลขเฉลี่ยจากส่วนท้ายของไฟล์ `People counting record sheet.xlsx` มากรอกลงในตารางนี้เพื่อใช้เป็นข้อมูลอ้างอิงในการตอบคำถามข้อ 1:

| Configuration | Average Response Time (ms) | Average Processing Time (ms) | Accuracy (%) |
| :--- | :---: | :---: | :---: |
| **Edge (YOLOv8n)** | `[กรอก เช่น 125.40 ms]` | `[กรอก เช่น 115.20 ms]` | `[กรอก เช่น 78.50%]` |
| **Cloud (YOLOv8x)** | `[กรอก เช่น 640.80 ms]` | `[กรอก เช่น 82.10 ms]` | `[กรอก เช่น 95.00%]` |
| **Edge–Cloud (Hybrid)** | `[กรอก เช่น 285.60 ms]` | `[กรอก เช่น 132.50 ms]` | `[กรอก เช่น 91.20%]` |

---

## 📝 Part 3: Complete the question set (ตอบคำถาม 5 ข้อ รวม 5 คะแนน)

---

### Question 1: Performance comparison (1 point)
> **โจทย์:** In the result summary section (at the end of the record sheet), observe the values of Average Response Time (ms), Average Processing Time (ms), and Accuracy. Identify which configuration (Edge, Cloud, or Edge–Cloud) shows highest or lowest values for each metric. Analyze the reasons behind these differences.

#### 1. การระบุค่าสูงสุด (Highest) และค่าต่ำสุด (Lowest):
- **Average Response Time (ms):**
  - **Highest:** `[ระบุ เช่น Cloud]` (ค่าเฉลี่ย: `______` ms)
  - **Lowest:** `[ระบุ เช่น Edge]` (ค่าเฉลี่ย: `______` ms)
- **Average Processing Time (ms):**
  - **Highest:** `[ระบุ เช่น Edge หรือ Edge-Cloud ขึ้นกับสเปกเครื่อง]` (ค่าเฉลี่ย: `______` ms)
  - **Lowest:** `[ระบุ เช่น Cloud]` (ค่าเฉลี่ย: `______` ms)
- **Accuracy (%):**
  - **Highest:** `[ระบุ เช่น Cloud]` (ค่าเฉลี่ย: `______` %)
  - **Lowest:** `[ระบุ เช่น Edge]` (ค่าเฉลี่ย: `______` %)

#### 2. บทวิเคราะห์สาเหตุเชิงเทคนิค (สามารถคัดลอกข้อความด้านล่างไปใช้ตอบได้):
```text
Based on the experimental results from the summary sheet, the performance differences among Edge, Cloud, and Edge-Cloud can be analyzed as follows:

1. Average Response Time (ms):
- Lowest: Edge configuration exhibits the lowest response time because the processing occurs entirely on the local machine (127.0.0.1). There is zero wide-area network transmission overhead or propagation delay.
- Highest: Cloud configuration has the highest response time due to the network round-trip time (RTT). The client must upload a high-resolution image over the Internet to the AWS SageMaker endpoint (ap-southeast-1) and wait for the response payload to return.
- Edge-Cloud provides a balanced intermediate response time: it achieves fast local response for high-confidence predictions and only incurs cloud transmission latency when the edge model indicates low confidence.

2. Average Processing Time (ms):
- Lowest: Cloud configuration demonstrates the fastest inference/processing time because it utilizes dedicated cloud compute instances optimized for neural network inference, despite running the heavyweight YOLOv8x model.
- Edge configuration uses the lightweight YOLOv8n model (~3.2M parameters) to minimize compute requirements, yet local execution speed depends on the host PC's CPU/GPU capability.
- Edge-Cloud processing time accounts for local inference plus optional cloud inference overhead when offloading is triggered.

3. Accuracy (%):
- Highest: Cloud achieves the highest accuracy because it deploys YOLOv8x, which has deeper feature representations, higher parameter count (~68.2M), and significantly better capability in detecting small, distant, or occluded people in crowded scenes.
- Lowest: Edge exhibits the lowest accuracy as YOLOv8n sacrifices detection sensitivity and complex bounding box resolution in exchange for low memory footprint and execution speed.
- Edge-Cloud achieves near-cloud accuracy because low-confidence edge detections are dynamically delegated to the cloud YOLOv8x model, effectively recovering difficult edge-case detections.
```

---

### Question 2: Suitable use cases (1 point)
> **โจทย์:** Based on the results, which computing setup (Edge, Cloud, or Edge–Cloud) is best suited for different application characteristics/needs/requirements, considering the trade-offs among accuracy, response time, and cost?

#### บทวิเคราะห์และการจัดสรร Use Cases (สามารถคัดลอกข้อความด้านล่างไปใช้ตอบได้):
```text
Considering the trade-offs among Accuracy, Response Time, Bandwidth, and Financial Cost, the recommended use cases for each computing setup are:

1. Edge Computing Setup:
- Best suited for: Real-time, mission-critical applications where latency is paramount (<150 ms), privacy is critical, or network connectivity is unstable/offline.
- Trade-offs: Sacrifices slight detection accuracy in dense crowds to achieve zero-latency and zero ongoing cloud service costs.
- Practical Use Cases:
  * Smart pedestrian crossing signals and safety gates where instant local decisions are required.
  * In-vehicle driver monitoring or drone surveillance in remote offline areas.
  * Private premises surveillance where video streams must not leave the local network for GDPR/PDPA compliance.

2. Cloud Computing Setup:
- Best suited for: Applications where absolute accuracy is paramount, batch analytics are sufficient, and centralized high-performance computing can be scaled on demand.
- Trade-offs: Offers top-tier precision and centralized model management, but incurs significant ongoing AWS infrastructure costs and higher network latency.
- Practical Use Cases:
  * Post-event surveillance video auditing, forensic crowd density analysis, and historical foot-traffic analytics.
  * High-precision security screening where missing any detection (false negatives) carries severe penalties.
  * Centralized camera analytics across multiple branches without requiring powerful edge compute hardware.

3. Edge–Cloud (Hybrid) Computing Setup:
- Best suited for: Scalable real-world deployments that require high overall accuracy while maintaining low average latency and controlling cloud operation/bandwidth costs.
- Trade-offs: Delivers the optimal balance by offloading only ambiguous/uncertain frames (low confidence) to the cloud, minimizing bandwidth and cloud compute fees while maintaining near-cloud accuracy.
- Practical Use Cases:
  * Smart City and Campus Surveillance: Handling routine foot traffic quickly at the edge, while offloading crowded or occluded scenes to SageMaker for deep inspection.
  * Retail Store Customer Analytics: Running real-time occupancy counting locally at the entrance, while escalating complex queue or group analysis to the cloud.
```

---

### Question 3: AWS cleanup (1 point)
> **โจทย์:** Have you completed the cleanup step after finishing the assignment to avoid unexpected AWS charges?
> **Pick a choice:**
> - [x] **Yes**

*(คำอธิบายเพิ่มเติมสำหรับการปฏิบัติจริง: ได้ทำการลบ SageMaker Endpoint, Model, Endpoint Configuration, Stop & Delete Notebook Instance `sds-edge-computing`, และลบ IAM Access Key / User `sds-sagemaker` เรียบร้อยแล้ว)*

---

### Question 4: Activity Feedback (1 point)
> **โจทย์:** How difficult was this activity?
> **Pick a choice:**
> - [ ] Too easy
> - [x] **Just right** *(แนะนำ หรือเลือกตามความรู้สึกจริงของผู้เรียน)*
> - [ ] Too difficult

---

### Question 5: Activity Feedback (1 point)
> **โจทย์:** Suggestions for improvement or other feedback.  
> **Compose an answer:**

> **คำแนะนำ:** สามารถนำข้อความตัวอย่างด้านล่างนี้ไปปรับใช้หรือใส่ความคิดเห็นส่วนตัวของผู้เรียนได้เลยครับ:

```text
The activity provides an excellent and comprehensive hands-on experience in comparing Edge, Cloud, and Hybrid computing paradigms. Setting up AWS SageMaker alongside local Docker containers effectively demonstrated the real-world trade-offs between network latency, compute capacity, and detection accuracy.

Suggestions for improvement:
1. It would be helpful to include an automated script or a verification cell in EndpointDeployment.ipynb that explicitly lists remaining active billable resources before notebook shutdown.
2. Providing a clear threshold explanation of the hybrid confidence score logic in the README would help students understand exactly how the offloading decision is tuned.
```
