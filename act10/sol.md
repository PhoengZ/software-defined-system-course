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
![alt text](image.png)
```

---

### Slot 2: `Screenshot “Welcome to People Counting Services” (Webpage)`
> **คำแนะนำ:** แคปภาพหน้าจอเว็บแอปพลิเคชันที่ URL `http://localhost:5173/` หลังจากสั่งรัน `docker compose up --build` สำเร็จและเบราว์เซอร์เปิดหน้าเว็บขึ้นมาได้

```markdown
<!-- วางรูปภาพที่นี่ (บันทึกเป็นชื่อ webpage_service.png ในโฟลเดอร์เดียวกัน) -->
![alt text](image-1.png)
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
| **Edge (YOLOv8n)** | `1,304.89 ms` | `1,247.03 ms` | `94.20%` |
| **Cloud (YOLOv8x)** | `2,136.12 ms` | `1,773.48 ms` | `100.00%` |
| **Edge–Cloud (Hybrid)** | `1,942.47 ms` | `1,885.78 ms` | `97.00%` |

---

## 📝 Part 3: Complete the question set (ตอบคำถาม 5 ข้อ รวม 5 คะแนน)

---

### Question 1: Performance comparison (1 point)
> **โจทย์:** In the result summary section (at the end of the record sheet), observe the values of Average Response Time (ms), Average Processing Time (ms), and Accuracy. Identify which configuration (Edge, Cloud, or Edge–Cloud) shows highest or lowest values for each metric. Analyze the reasons behind these differences.

#### 1. การระบุค่าสูงสุด (Highest) และค่าต่ำสุด (Lowest):
- **Average Response Time (ms):**
  - **Highest:** `Cloud` (ค่าเฉลี่ย: `2,136.12` ms)
  - **Lowest:** `Edge` (ค่าเฉลี่ย: `1,304.89` ms)
- **Average Processing Time (ms):**
  - **Highest:** `Edge-Cloud` (ค่าเฉลี่ย: `1,885.78` ms)
  - **Lowest:** `Edge` (ค่าเฉลี่ย: `1,247.03` ms)
- **Accuracy (%):**
  - **Highest:** `Cloud` (ค่าเฉลี่ย: `100.00` %)
  - **Lowest:** `Edge` (ค่าเฉลี่ย: `94.20` %)

#### 2. บทวิเคราะห์สาเหตุเชิงเทคนิค (สามารถคัดลอกข้อความด้านล่างไปใช้ตอบได้ทันที):
```text
จากผลการทดลองในแถบ Result Summary สรุปการเปรียบเทียบในแต่ละ Metric ได้ดังนี้:

1. Average Response Time (ms):
- ต่ำที่สุด (Lowest): Edge (เฉลี่ย 1,304.89 ms)
  เหตุผล: Edge ประมวลผลทุกอย่างอยู่ภายในเครื่อง Local PC เองทั้งหมด (127.0.0.1) ไม่มีการส่งข้อมูลรูปภาพขนาดใหญ่ออกไปยังภายนอก จึงไม่มีค่า Network Latency หรือเวลาหน่วงจากการส่งผ่านเครือข่ายเลย
- สูงที่สุด (Highest): Cloud (เฉลี่ย 2,136.12 ms)
  เหตุผล: ฝั่ง Cloud ต้องเจอกับ Network Round-Trip Time (RTT) เพราะเครื่องลูกข่ายต้องบีบอัดรูปภาพแล้วอัปโหลดผ่านระบบอินเทอร์เน็ตไปยัง AWS SageMaker Endpoint ที่ต่างประเทศ แล้วรอรับข้อมูลผลลัพธ์กลับมา ทำให้เสียเวลาเดินทางบนเครือข่ายเป็นหลัก
* ส่วน Edge-Cloud ได้ค่าเฉลี่ย 1,942.47 ms อยู่ในระดับปานกลาง เนื่องจากบางรูปที่มีความมั่นใจสูงจะประมวลผลจบที่เครื่องตัวเองได้ทันที แต่ถ้ารูปไหนตรวจจับได้ยาก ระบบจะส่งต่อขึ้น Cloud ทำให้เวลาเฉลี่ยถูกดึงขึ้นมาอยู่ตรงกลาง

2. Average Processing Time (ms):
- ต่ำที่สุด (Lowest): Edge (เฉลี่ย 1,247.03 ms)
  เหตุผล: Edge รันด้วยโมเดลขนาดเล็กอย่าง YOLOv8n (มีพารามิเตอร์เพียงประมาณ 3.2M) ซึ่งถูกออกแบบมาให้โครงข่ายมีความซับซ้อนต่ำ คำนวณได้เบาและรวดเร็วบนซีพียูทั่วไป
- สูงที่สุด (Highest): Edge-Cloud (เฉลี่ย 1,885.78 ms)
  เหตุผล: ในกรณีที่รูปภาพมีคนหนาแน่นหรือมีความกำกวม ระบบของ Edge-Cloud จะต้องทำการรันโมเดลเล็กที่ Edge ให้เสร็จก่อนหนึ่งรอบ จากนั้นเมื่อพบว่าค่าความมั่นใจ (Confidence) ต่ำกว่าเกณฑ์ที่กำหนด จึงจำเป็นต้องส่งรูปภาพไปให้โมเดลใหญ่ YOLOv8x บน Cloud คำนวณซ้ำอีกครั้ง ส่งผลให้เวลาประมวลผลกลายเป็นการบวกเวลาระหว่างทั้งสองระบบรวมกัน
* ขณะที่ Cloud รันโมเดลตัวใหญ่ YOLOv8x (มีพารามิเตอร์ 68.2M) ตัวเดียวบนทรัพยากร vCPU ของ SageMaker ทำให้ใช้เวลาประมวลผลคงที่อยู่ที่ประมาณ 1,773.48 ms

3. Average Accuracy (%):
- สูงที่สุด (Highest): Cloud (เฉลี่ย 100.00%)
  เหตุผล: โมเดล YOLOv8x บน Cloud มีสถาปัตยกรรมโครงข่ายประสาทเทียมที่ลึกและมีจำนวนพารามิเตอร์สูงมาก ทำให้สามารถสกัดฟีเจอร์และจับรายละเอียดที่ซับซ้อน เช่น คนที่ยืนซ้อนกัน คนที่ตัวเล็ก หรือคนที่อยู่ไกลได้อย่างครบถ้วนโดยไม่มีการตรวจหลุด
- ต่ำที่สุด (Lowest): Edge (เฉลี่ย 94.20%)
  เหตุผล: โมเดล YOLOv8n ตัดทอนเลเยอร์ลงเพื่อแลกกับความเร็ว ทำให้ความละเอียดในการวาด Bounding Box ลดลง ส่งผลให้ในภาพที่มีคนแออัดหรือยืนบังกัน (เช่น รูปที่ 2 ตรวจได้ 6 จาก 9 คน และรูปที่ 4 ตรวจได้ 16 จาก 24 คน) มีคนบางส่วนที่โมเดลตรวจจับไม่พบ
* ทั้งนี้ Edge-Cloud สามารถทำความแม่นยำเฉลี่ยได้สูงถึง 97.00% เพราะมีกลไกตรวจสอบความมั่นใจ เมื่อโมเดลเล็กไม่แน่ใจ ระบบจะส่งภาพไปให้ Cloud ช่วยยืนยันผล จึงสามารถกู้คืนเคสที่ Edge พลาดไปให้กลับมาตรวจจับได้ถูกต้องเกือบเทียบเท่า Cloud
```

---

### Question 2: Suitable use cases (1 point)
> **โจทย์:** Based on the results, which computing setup (Edge, Cloud, or Edge–Cloud) is best suited for different application characteristics/needs/requirements, considering the trade-offs among accuracy, response time, and cost?

#### บทวิเคราะห์และการจัดสรร Use Cases (สามารถคัดลอกข้อความด้านล่างไปใช้ตอบได้ทันที):
```text
เมื่อพิจารณาข้อดีข้อเสีย (Trade-offs) ทั้ง 4 ด้าน ได้แก่ ความแม่นยำ (Accuracy), ความเร็วในการตอบสนอง (Response Time), ปริมาณแบนด์วิธ (Bandwidth) และค่าใช้จ่าย (Cost) การเลือกใช้งานแต่ละระบบมีความเหมาะสมกับลักษณะงานดังต่อไปนี้:

1. Edge Computing Setup (เหมาะกับงานที่ต้องการความเร็วระดับ Real-time, ออฟไลน์ และต้องการความเป็นส่วนตัวสูง):
- จุดเด่นและข้อแลกเปลี่ยน: มี Response Time ต่ำที่สุดและไม่มีค่าใช้จ่ายบริการคลาวด์รายเดือน ข้อมูลภาพไม่รั่วไหลออกนอกสถานที่ (ตอบโจทย์กฎหมาย PDPA/ความเป็นส่วนตัว) แต่ต้องยอมรับความแม่นยำที่ลดลงบ้างในสถานการณ์ที่มีคนแออัด
- งานที่เหมาะสม:
  * ระบบไฟข้ามถนนอัจฉริยะและประตูกั้นชานชาลาอัตโนมัติ: ต้องตัดสินใจแบบเรียลไทม์ทันทีเพื่อความปลอดภัย หน่วงเวลาไม่ได้แม้แต่วินาทีเดียว
  * กล้องตรวจจับในพื้นที่ห่างไกล หรือบนโดรนสำรวจ: สัญญาณอินเทอร์เน็ตไม่เสถียรหรือไม่มีการเชื่อมต่อเครือข่าย ต้องสามารถทำงานแบบ Offline ได้
  * ระบบกล้องในพื้นที่ความลับสูงหรือห้องส่วนบุคคล: เช่น โรงพยาบาล หรือโรงงานวิจัย ที่มีนโยบายห้ามส่งข้อมูลภาพออกนอกเครือข่ายภายใน

2. Cloud Computing Setup (เหมาะกับงานที่ต้องการความถูกต้องแม่นยำสูงสุด หรืองานวิเคราะห์ข้อมูลย้อนหลัง):
- จุดเด่นและข้อแลกเปลี่ยน: ให้ความแม่นยำสูงที่สุด (Accuracy 100%) รองรับโมเดลขนาดใหญ่ และสามารถรวมศูนย์ข้อมูลจากหลายจุดเข้ามาที่เดียวได้ง่าย แต่ต้องแลกกับความเร็วในการตอบสนองที่ช้ากว่าเนื่องจากติดปัญหา Network Latency และมีค่าใช้จ่ายเซิร์ฟเวอร์คลาวด์ต่อเนื่องตามระยะเวลาที่เปิดใช้งาน
- งานที่เหมาะสม:
  * การตรวจนับสถิติคนและความหนาแน่นย้อนหลัง (Foot-traffic Analytics & Audit): นำวิดีโอจากหลายสาขามาประมวลผลสรุปยอดคนประจำวัน ซึ่งไม่จำเป็นต้องทราบผลทันที แต่ต้องการตัวเลขที่แม่นยำที่สุด
  * ระบบรักษาความปลอดภัยขั้นสูง (High-security Screening): เช่น สนามบิน หรือเรือนจำ ที่ยอมรับความผิดพลาดในการตรวจจับ (False Negative) ไม่ได้เลยแม้แต่คนเดียว
  * ระบบกล้องวงจรปิดของสาขาย่อยจำนวนมาก: หน้าร้านใช้กล้องธรรมดา แล้วส่งภาพมารวมวิเคราะห์ที่คลาวด์ส่วนกลาง ช่วยให้ดูแลและอัปเดตโมเดลเวอร์ชันใหม่ได้พร้อมกันทุกสาขา

3. Edge–Cloud Computing Setup (Hybrid) (เหมาะกับระบบ Smart City และธุรกิจที่ต้องการสมดุลความเร็ว ความแม่นยำ และคุมงบประมาณ):
- จุดเด่นและข้อแลกเปลี่ยน: เป็นสถาปัตยกรรมที่ลงตัวที่สุดสำหรับระบบจริง เพราะภาพส่วนใหญ่ที่ตรวจจับได้ง่ายจะจบที่ Edge ทันที ช่วยประหยัดแบนด์วิธและลดจำนวนครั้งที่ต้องเรียกใช้คลาวด์ และจะส่งขึ้น Cloud เฉพาะภาพที่โมเดลเล็กไม่มั่นใจเท่านั้น ทำให้ได้ความแม่นยำสูงถึง 97% ในขณะที่ควบคุมค่าใช้จ่ายคลาวด์ได้ดีเยี่ยม
- งานที่เหมาะสม:
  * ระบบกล้องตรวจนับคนในมหาวิทยาลัยและห้างสรรพสินค้า (Smart Campus & Smart Retail): วันปกติที่คนเดินกระจายตัวกัน Edge จะนับและแสดงผลได้ทันที แต่เมื่อถึงช่วงเทศกาลหรือจุดที่มีคนยืนบังกัน ระบบจะส่งภาพขึ้น SageMaker ไปวิเคราะห์อย่างละเอียด
  * ระบบเมืองอัจฉริยะ (Smart City Surveillance): กล้องประจำเสาไฟตรวจนับคนและยานพาหนะทั่วไปที่หน้างาน และจะส่งเฉพาะภาพเหตุการณ์แปลกๆ ภาพที่มีหมอกควันหนาแน่น หรือภาพที่ไม่ชัดเจนขึ้นคลาวด์เพื่อยืนยันผลซ้ำ
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
