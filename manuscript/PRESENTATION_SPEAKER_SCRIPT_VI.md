# Kịch Bản Thuyết Trình Tiếng Việt Cho Bài Báo

## Mục tiêu của kịch bản

Tài liệu này là kịch bản nói tiếng Việt cho một bài thuyết trình seminar khoảng 15-20 phút về bài báo:

**Label Realism, Data Governance, and Representation Shift: Revisiting ML-Based TCP in Continuous Integration**

Kịch bản này được viết theo bốn nguyên tắc:

1. Bám chặt vào lập luận thật của bài báo.
2. Phân biệt đúng mức độ bằng chứng giữa phần đã có kết quả thực thi, phần là framework, và phần đang ở mức staged extension.
3. Trình bày theo giọng seminar rõ ràng, dễ hiểu, nhìn slide lớn là nói được ngay.
4. Giữ nhịp nói tự tin, mạch lạc, có kết luận mạnh và dễ nhớ.

Thời lượng mục tiêu: **17-18 phút**.

---

## Cấu trúc gợi ý cho slide

1. Tiêu đề và câu hỏi trung tâm
2. Bài toán TCP trong CI
3. Benchmark gốc đã kết luận điều gì
4. Khoảng trống mà bài báo này giải quyết
5. Bốn realism gaps
6. Thiết kế nghiên cứu và six-tier baseline grid
7. Direction A: label realism
8. Direction B: federated pretraining
9. Direction C: representation shift
10. Kết quả thực nghiệm của Direction C
11. Direction D: external validity / Android CI
12. Thảo luận và ý nghĩa thực tiễn
13. Kết luận

---

## Script chi tiết theo slide

## Slide 1 - Tiêu đề và câu hỏi trung tâm
**Thời lượng:** 1.0-1.5 phút

**Speaker script:**

Xin chào thầy cô và các bạn. Hôm nay nhóm chúng em trình bày bài báo về machine-learning-based test case prioritization trong continuous integration, hay nói ngắn gọn là ML-based TCP trong CI.

Tiêu đề bài báo là: *Label Realism, Data Governance, and Representation Shift: Revisiting ML-Based TCP in Continuous Integration*.

Điểm xuất phát của bài này rất rõ: chúng em không đi từ một benchmark yếu, mà đi từ một benchmark mạnh, có ảnh hưởng lớn, và đã định hình cách cộng đồng nhìn về ML-TCP trong CI.

Từ đó, bài báo đặt ra một câu hỏi trung tâm rất trực diện:

**Nếu một kết luận đúng trong benchmark, thì khi đưa sang bối cảnh triển khai thực tế, kết luận đó còn đáng tin đến mức nào?**

Nói cách khác, bài báo này không chỉ hỏi “phương pháp nào thắng”, mà hỏi một câu quan trọng hơn nhiều đối với người làm hệ thống:

**Khi nào thì khuyến nghị từ benchmark có thể mang đi deploy, khi nào cần bổ sung điều kiện, và khi nào phải hiệu chỉnh lại?**

Đó là tinh thần xuyên suốt của toàn bộ bài báo.

**Chuyển slide:**

Để thấy vì sao câu hỏi này quan trọng, trước hết em xin nhắc nhanh bài toán gốc mà cộng đồng đang cùng quan tâm.

---

## Slide 2 - Bài toán TCP trong CI
**Thời lượng:** 1.0-1.5 phút

**Speaker script:**

Trong continuous integration, mỗi lần có commit mới, hệ thống sẽ build lại và chạy test lại. Vấn đề là regression testing rất tốn thời gian, trong khi giá trị của CI lại nằm ở chỗ phản hồi phải đến sớm.

TCP, tức test case prioritization, giải quyết đúng điểm nghẽn này bằng cách sắp lại thứ tự test để những lỗi hữu ích xuất hiện càng sớm càng tốt.

Nếu thứ tự tốt, developer có feedback sớm, sửa lỗi nhanh hơn, và pipeline giữ được giá trị vận hành. Nếu thứ tự kém, test vẫn chạy, nhưng giá trị thực tế giảm mạnh vì lỗi quan trọng xuất hiện quá muộn.

Vì vậy, trong CI, TCP không chỉ là bài toán xếp hạng. Nó là bài toán xếp hạng dưới áp lực thời gian, nhiễu, và yêu cầu phản hồi nhanh.

**Chuyển slide:**

Từ bài toán đó, benchmark gốc mà bài báo này dựa vào đã đưa ra những kết luận rất có sức nặng.

---

## Slide 3 - Benchmark gốc đã kết luận điều gì
**Thời lượng:** 1.5 phút

**Speaker script:**

Benchmark gốc mà chúng em lấy làm điểm xuất phát là bài của Zhao và cộng sự, ICSME 2023. Bài này đánh giá 11 kỹ thuật ML-based TCP trên 11 đối tượng, dưới một quy trình benchmark thống nhất.

Từ benchmark đó, có ba kết luận lớn.

Thứ nhất, **không có universal winner**. Không có một phương pháp thắng ở mọi nơi.

Thứ hai, **khuyến nghị phụ thuộc vào failure regime**. Tức là khi đặc trưng fail của dữ liệu thay đổi, phương pháp nên dùng cũng có thể thay đổi theo.

Thứ ba, **cross-subject pretraining có giá trị vận hành rất lớn**. Cụ thể, pretraining có thể nâng khả năng đạt thứ tự tối ưu từ khoảng 50% lên 80%.

Đây là những kết luận rất mạnh, và quan trọng hơn, chúng dẫn thẳng tới các khuyến nghị có thể dùng trong thực tế, xoay quanh MART, ACER-PA, PPO-based methods và chiến lược pretraining.

Điểm mà bài báo của chúng em nhấn mạnh là thế này: các khuyến nghị đó được rút ra trong điều kiện benchmark. Câu hỏi tiếp theo phải là: **khi điều kiện benchmark không còn giữ nguyên, độ bền của các khuyến nghị đó còn lại bao nhiêu?**

---

## Slide 4 - Khoảng trống mà bài báo này giải quyết
**Thời lượng:** 1.0-1.5 phút

**Speaker script:**

Đóng góp trung tâm của bài báo này là chuyển trọng tâm từ leaderboard sang reliability.

Chúng em không đi theo hướng “thêm một model mới rồi tuyên bố model này vượt tất cả”. Chúng em cũng không đi theo hướng bác bỏ benchmark gốc.

Thay vào đó, bài báo đưa ra một khung nhìn mới, gọi là **conditional-validity map**.

Bản đồ này trả lời ba câu hỏi rất thực dụng:

- Kết luận nào của benchmark vẫn giữ nguyên?
- Kết luận nào chỉ đúng khi một số giả định được thỏa mãn?
- Và kết luận nào có thể suy yếu, đổi hướng, hoặc đảo chiều khi realism constraints được áp vào?

Nói ngắn gọn, bài báo này thay đổi câu hỏi cốt lõi từ “ai tốt nhất?” sang “khi nào thì lời khuyên này thật sự đáng tin?”.

**Chuyển slide:**

Để làm được điều đó, bài báo tổ chức toàn bộ vấn đề thành bốn realism gaps rất rõ ràng.

---

## Slide 5 - Bốn realism gaps
**Thời lượng:** 2.0 phút

**Speaker script:**

Bốn realism gaps chính là xương sống của bài báo.

**Gap thứ nhất là label realism.**
Trong CI thực tế, không phải mọi fail đều là regression thật. Một phần có thể là flaky. Nếu mô hình học từ nhãn nhiễu, thì nó có thể học sai tín hiệu cần thiết.

**Gap thứ hai là data governance.**
Benchmark gốc cho thấy pretraining rất mạnh, nhưng sức mạnh đó đi kèm một giả định lớn: có thể gom raw execution histories lại để huấn luyện. Trong môi trường thật, giả định này thường không đứng vững.

**Gap thứ ba là representation realism.**
Benchmark gốc được xây trên handcrafted CI features. Nhưng hệ thống hiện đại ngày càng dùng semantic representations và code embeddings. Khi representation thay đổi, ranking có thể thay đổi theo.

**Gap thứ tư là external validity.**
Kết luận rút ra từ các benchmark Java/C ổn định có còn giữ được khi chuyển sang những môi trường khó hơn, nhiễu hơn, đắt đỏ hơn, như long-running suites hoặc Android/mobile CI hay không?

Bốn gap này không phải bốn mảnh rời rạc. Khi đặt cùng nhau, chúng cho thấy một điều rất quan trọng: benchmark có thể sạch về phương pháp, nhưng vẫn có thể quá tự tin nếu ta biến kết quả benchmark thành lời khuyên deployment mà không qua bước kiểm định bổ sung.

---

## Slide 6 - Thiết kế nghiên cứu và six-tier baseline grid
**Thời lượng:** 1.5 phút

**Speaker script:**

Về mặt thiết kế thực nghiệm, bài báo đặt ra một yêu cầu rất chặt: mọi bảng kết quả chính đều phải so sánh trên một baseline grid gồm 6 tầng.

Lý do rất đơn giản. Nếu chỉ so một phương pháp mới với một nhóm baseline hẹp, thì rất dễ tạo ra một kết luận đẹp nhưng không đủ sức nặng.

Sáu tầng mà bài báo yêu cầu gồm:

1. Heuristic và non-ML similarity methods, với FAST là đại diện nổi bật.
2. Các CI heuristics đơn giản.
3. Semantic baseline, cụ thể ở đây là FALCON.
4. Deep learning TCP, như DeepOrder.
5. Nhóm ML/RL của source paper, gồm MART, ACER-PA, PPO1-LI, PPO2-PO và các method liên quan.
6. Các biến thể mới do bài báo này đưa vào.

Điểm mạnh của thiết kế này là: bài báo không cho phép một kết quả mới “đẹp” chỉ vì đối thủ quá yếu. Mọi kết luận đều phải đứng được trên toàn bộ mặt bằng cạnh tranh.

---

## Slide 7 - Direction A: label realism
**Thời lượng:** 1.5 phút

**Speaker script:**

Direction A đi thẳng vào một câu hỏi rất mạnh:

**Nếu nhãn trong CI bị flaky contamination, thì đánh giá ML-TCP có bị lệch đến mức làm thay đổi khuyến nghị chọn phương pháp hay không?**

Đây là một hướng rất quan trọng, vì toàn bộ họ ML/RL trong TCP đều học từ lịch sử fail. Nếu lịch sử đó chứa nhiều fail giả, thì ranking học được có thể bị kéo lệch ngay từ nền móng.

Trong phiên bản manuscript hiện tại, Direction A được đóng gói như một protocol rất rõ ràng:

- xây flaky-label subsets bằng re-execution và CI-log mining,
- so sánh raw APFD với cleaned APFD,
- và đo xem phương pháp nào nhạy nhất trước nhiễu nhãn.

Điểm đáng nói ở đây là bài báo không né vấn đề. Bài báo đặt label quality lên đúng vị trí của nó: **nếu nhãn không sạch, thì độ tin cậy của khuyến nghị cũng không thể được xem là mặc định**.

---

## Slide 8 - Direction B: federated pretraining
**Thời lượng:** 1.5 phút

**Speaker script:**

Direction B nhắm thẳng vào phát hiện có giá trị thực tiễn lớn nhất của benchmark gốc: lợi ích rất mạnh của pretraining.

Nếu benchmark gốc cho thấy pretraining giúp tăng từ khoảng 50% lên 80% khả năng đạt thứ tự tối ưu, thì câu hỏi kế tiếp không còn là “pretraining có tốt không”, mà là:

**Làm thế nào để giữ được lợi ích đó trong bối cảnh dữ liệu không thể pooling một cách tùy ý?**

Và đó chính là vai trò của federated pretraining.

Direction B đặt ra một mục tiêu rất rõ: biến lợi ích của pretraining thành thứ có thể deploy được trong môi trường có ràng buộc về governance.

Hypothesis chính của bài báo là federated pretraining có thể giữ được ít nhất 70% lợi ích của centralized transfer. Nếu điều này đúng, thì ý nghĩa thực tế rất lớn: pretraining không còn là đặc quyền của những môi trường được phép gom toàn bộ raw CI histories về một chỗ.

Nói ngắn gọn, Direction B mở đường để chuyển một kết quả mạnh trong benchmark thành một khuyến nghị khả thi hơn trong triển khai thật.

---

## Slide 9 - Direction C: representation shift
**Thời lượng:** 1.5 phút

**Speaker script:**

Direction C là hướng có kết quả thực nghiệm rõ nhất trong manuscript hiện tại.

Động lực của Direction C rất mạnh và rất cơ bản: mọi bảng xếp hạng method thực chất đều phụ thuộc vào representation mà ta dùng để nhìn bài toán.

Source paper xếp hạng các method trên handcrafted features. Nhưng nếu thay representation bằng LLM-derived embeddings, thì thứ tự xếp hạng có thể thay đổi, và khi đó, các khuyến nghị mang tính operational từ benchmark gốc cũng có thể phải xem lại.

Đây chính là chỗ mà bài báo dùng khái niệm **feature-era artifact**. Tức là có những kết luận có thể đúng trong kỷ nguyên feature pipeline cũ, nhưng chưa chắc còn đứng vững khi representation đổi sang semantic space hiện đại hơn.

FALCON ở đây là mốc tham chiếu rất quan trọng, vì nó cho thấy semantic representations có thể tạo ra mức hiệu quả đủ lớn để buộc cộng đồng phải đánh giá lại mặt bằng cạnh tranh.

Vì vậy, Direction C không chỉ hỏi “embedding có tốt hơn không”, mà hỏi một câu khó hơn và giá trị hơn:

**Khi representation thay đổi, các khuyến nghị vận hành cũ có còn giữ được không?**

---

## Slide 10 - Kết quả thực nghiệm của Direction C
**Thời lượng:** 2.5-3.0 phút

**Speaker script:**

Đây là slide kết quả quan trọng nhất của bài báo hiện tại.

Trước hết, em nói rất rõ về representation đã dùng. Do ràng buộc mạng tại thời điểm thực nghiệm, nhóm chưa lấy được full contextual UniXcoder vectors. Vì vậy, thí nghiệm hiện tại dùng một **vocabulary-anchored BPE proxy**, tức là một lower bound có chủ ý cho representation effect.

Trên 5 SIR subjects và 2.938 test cases, nhóm thử ba rankers:

- centroid similarity,
- logistic regression,
- và một MLP hai lớp,

rồi so sánh trực tiếp với FAST-pw.

Kết quả trung bình rất dứt khoát:

- MLP đạt mean APFD **0.5334**,
- FAST-pw đạt **0.8617**,
- và mean delta APFD là **-0.3283**.

Không chỉ thua, mà thua với khoảng cách lớn, rõ ràng và có ý nghĩa thống kê:

- 95% bootstrap CI là **[-0.4866, -0.1699]**, không cắt qua 0,
- Cohen’s d là **-1.94**, tức effect size lớn,
- mean Spearman rho là **-0.060**, nghĩa là gần như không có tương quan xếp hạng với FAST-pw.

Thông điệp khoa học ở đây cần nói thật gọn và thật chắc:

**Kết quả này bác bỏ ý tưởng rằng BPE-projection embeddings ở mức vocabulary-level có thể thay thế hiệu quả cho handcrafted signal trong bộ dữ liệu này.**

Đây là một negative result, nhưng là negative result rất có giá trị. Nó nói với chúng ta rằng không phải cứ “LLM-flavored” là tự động tốt hơn.

Đồng thời, kết quả này cũng làm rõ thêm vai trò của FALCON: FALCON vẫn là mốc tham chiếu cho semantic representation effect ở trần cao hơn, còn proxy hiện tại là một lower-bound result cho thấy nếu representation quá yếu, ranking sẽ không giữ được chất lượng.

Vì vậy, Direction C không làm yếu luận điểm của bài báo. Ngược lại, nó làm luận điểm mạnh hơn: **representation shift thật sự có sức thay đổi kết luận, và vì thế nó phải được kiểm định nghiêm túc, chứ không thể xem như chi tiết phụ.**

---

## Slide 11 - Direction D: external validity / Android CI
**Thời lượng:** 1.0-1.5 phút

**Speaker script:**

Direction D đưa bài toán ra bối cảnh khó hơn, với đích nhắm rõ nhất là Android/mobile CI.

Lý do Direction D quan trọng là vì Android CI khác benchmark gốc trên nhiều trục cùng lúc:

- emulator-induced flakiness,
- hardware heterogeneity,
- per-test setup cost cao,
- và time window ngắn hơn.

Những khác biệt này không chỉ làm bài toán “khó hơn một chút”. Chúng có thể làm thay đổi chính giả định nền mà benchmark gốc đang dựa vào.

Trong manuscript hiện tại, Direction D được tổ chức như một staged extension có protocol rõ ràng. Điểm mạnh ở đây là bài báo không né external validity, mà chủ động khóa tiêu chuẩn đầu vào cho một bài kiểm định khó hơn, thay vì tuyên bố vượt trước bằng chứng.

Tạm thời, LRTS được dùng như một stress case trong Java; còn Android là hard endpoint mà bài báo đã xác định rất rõ hướng đi.

---

## Slide 12 - Thảo luận và ý nghĩa thực tiễn
**Thời lượng:** 2.0 phút

**Speaker script:**

Nếu phải tóm gọn ý nghĩa thực tiễn của bài báo trong vài câu, em sẽ nói thế này.

Thứ nhất, **benchmark result không tự động bằng deployment recommendation**.

Thứ hai, để đưa một khuyến nghị vào môi trường thật, có bốn nhóm điều kiện bắt buộc phải kiểm tra:

- nhãn có sạch hay không,
- dữ liệu có được phép pooling hay không,
- representation đã đổi hay chưa,
- và môi trường triển khai còn giống benchmark hay không.

Thứ ba, bài báo này không phá benchmark gốc. Bài báo giữ nguyên giá trị của benchmark gốc, giữ nguyên giá trị của FAST, FALCON, các source-paper methods, và toàn bộ mặt bằng cạnh tranh mà benchmark đã thiết lập.

Nhưng bài báo bổ sung một tầng rất quan trọng: **tầng qualification**.

Nói một cách trực diện, trước bài báo này, ta có benchmark và khuyến nghị. Sau bài báo này, ta có benchmark, khuyến nghị, và điều kiện để biết khi nào những khuyến nghị đó thật sự đáng tin.

Điểm mà manuscript hiện tại đã chốt rất mạnh ở phần thảo luận là một **deployment-facing conditional-validity matrix**. Ma trận này không hỏi “ai thắng tuyệt đối”, mà hỏi “trong điều kiện CI của mình, mình có quyền tin benchmark đến đâu”. Nếu môi trường gần với benchmark gốc, ta có thể dùng khuyến nghị đó với một bước kiểm tra nhẹ tại chỗ. Nhưng nếu flakiness cao, dữ liệu không được phép pooling, representation đã đổi sang semantic space, hoặc workload đã chuyển sang long-running hay mobile CI, thì khuyến nghị phải bị hạ cấp từ mặc định sang **provisional** cho đến khi có local stress test.

Đó chính là giá trị thực tiễn lớn nhất của conditional-validity map.

---

## Slide 13 - Kết luận
**Thời lượng:** 1.5 phút

**Speaker script:**

Để kết thúc, em xin gói bài báo này lại trong ba thông điệp.

**Thông điệp một:** benchmark ML-TCP của Zhao và cộng sự là mạnh, có giá trị, và xứng đáng là điểm xuất phát.

**Thông điệp hai:** các khuyến nghị rút ra từ benchmark đó là benchmark-valid, nhưng chưa mặc nhiên là deployment-valid.

**Thông điệp ba:** đóng góp lớn nhất của bài báo này là nâng chuẩn đánh giá ML-TCP từ leaderboard construction lên **conditional-validity certification**.

Nếu cần rút toàn bộ bài báo về một quy tắc triển khai rất ngắn, thì quy tắc đó là: trước khi mang một khuyến nghị ML-TCP đi deploy, hãy hỏi bốn câu. Nhãn fail có sạch không. Dữ liệu có được phép pooling không. Representation có đổi không. Và workload thực tế có còn giống benchmark không. Chỉ cần một câu trả lời là “chưa rõ”, thì benchmark recommendation phải được xem là điều kiện hóa, không phải mặc định.

Với manuscript hiện tại, phần executed mạnh nhất nằm ở Direction C, và kết quả ở đó cho thấy một điểm rất rõ: proxy embedding ở mức BPE token-level thua đáng kể FAST-pw trên 5 SIR subjects. Điều đó không đóng cánh cửa của semantic representations; điều đó buộc chúng ta phải phân biệt rành mạch giữa weak proxy và strong contextual representation.

Tổng kết lại, bài báo này không nổi bật vì đề xuất một model mới. Bài báo nổi bật vì nó đưa ra một **bản đồ độ tin cậy có điều kiện** cho những khuyến nghị của benchmark ML-TCP mạnh nhất hiện nay.

Em xin cảm ơn thầy cô và các bạn. Sau đây em rất sẵn sàng cho phần trao đổi.

---

## Bản rút gọn 30 giây để mở đầu nếu cần

Xin chào mọi người. Hôm nay em trình bày một bài báo xem xét lại benchmark ML-based TCP trong CI dưới bốn realism constraints: label realism, data governance, representation shift và external validity. Câu hỏi trung tâm của bài báo không phải là ai thắng benchmark, mà là khi nào khuyến nghị từ benchmark còn đủ mạnh để đem đi deploy. Kết quả executed rõ nhất hiện tại đến từ Direction C, nơi BPE-proxy embeddings thua đáng kể FAST-pw trên 5 SIR subjects. Đóng góp trung tâm của bài báo là một conditional-validity map, cụ thể hóa thành một ma trận quyết định giúp phân biệt khuyến nghị nào có thể dùng ngay và khuyến nghị nào còn phải stress-test tại chỗ.

---

## Bản rút gọn 45 giây để kết thúc nếu hết giờ

Nếu chỉ giữ lại một ý, thì đó là: **một benchmark result chưa đủ để trở thành deployment recommendation**. Bài báo này bổ sung lớp qualification cần thiết thông qua bốn realism gaps và biến nó thành một ma trận quyết định cho triển khai. Nó không phủ định benchmark gốc, mà xác định rõ miền mà benchmark còn đáng tin. Kết quả thực nghiệm hiện tại ở Direction C cho thấy representation proxy yếu có thể dẫn tới kết luận rất khác so với handcrafted baselines, và chính điều đó làm nổi bật giá trị của conditional-validity map. Em xin cảm ơn.

---

## Ghi chú cho người thuyết trình

1. Nói với giọng chắc, gọn, dứt câu; tránh xin lỗi hoặc tự hạ thấp kết quả.
2. Khi nói về Direction A, B, D, vẫn giữ đúng mức độ bằng chứng, nhưng không cần nói theo kiểu phòng thủ. Hãy nói đây là ba trục kiểm định cốt lõi mà bài báo chủ động mở ra.
3. Khi nói về Direction C, có thể xem đây là phần có kết quả thực nghiệm rõ và mạnh nhất trong manuscript hiện tại.
4. Nếu bị hỏi vì sao Direction C cho kết quả âm, câu trả lời nên là: proxy BPE ở mức vocabulary-level không đủ mạnh để thay thế handcrafted signal trên bộ dữ liệu này; đó là kết luận rõ ràng, hữu ích, và hoàn toàn có giá trị khoa học.
5. Nếu cần một câu chốt để người nghe nhớ lâu, hãy lặp lại câu này: **“Benchmark-valid không đồng nghĩa với deployment-valid.”**