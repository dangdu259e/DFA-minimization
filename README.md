# DFA-minimization

VNU - HUS - MIM - 2021

MAT3509 2 - Automata


## File: input.txt
    (Dữ liệu đầu vào)
    
    dòng 1: S -  Tập các trạng thái của otomat
    dòng 2: Sigma - bảng chữ cái đầu vào
    dòng 3: s0 - trạng thái khởi đầu (s0 thuộc S)
    dòng 4: F - tập trạng thái kết (F là tập con của S)  #note: vì một otomat có nhiều hàm chuyển nên có rất nhiều dòng 5, còn các dòng khác chỉ có 1 dòng duy nhất
    dòng 5- hết: các hàm chuyển trạng thái (có dạng: ví dụ (trạng thái bắt đầu, trạng thái đến, chữ cái)) (#note: mỗi dòng là 1 hàm chuyển)
    

    
## DFA-minimization: 2 cách

**Cách1**: lập trình bằng cách sử dụng thuật toán tối thiểu hoá otomat tài liệu cô đã cho.

- JUPYTER NOTEBOOK: [here](https://github.com/dangdu259e/DFA-minimization/blob/main/DFA-minimization.ipynb)
- PYTHON FILE: [here](https://github.com/dangdu259e/DFA-minimization/blob/main/DFA-minimization.py)

**Cách2**: Sử dụng thư viện pythomata => 
#### Cài đặt thư viện:
`$ pip install pythomata`


#### Nhận xét
- Ưu điểm: Cách 2 nhanh gọn vì đã được viết sẵn chỉ cần gọi hàm để thực hiện
- Nhược điểm: 
   + Cách 2 là dữ liệu đầu vào ở dạng SET (kiểu dữ liệu này là một tập giá trị không có thứ tự)
   + dữ liệu ở dạng set in ra màn hình sẽ bị lỗi hiển thị (xáo trộn vị trí các phần tử)
   + ouput đưa ra state tương ứng với các state gốc nhưng ở dạng số (do thư viện chưa format lại)
   + nếu in ra automaton gốc để dựa vào đó nhìn cách state tương ứng thì không được do state automaton gốc dạng set

