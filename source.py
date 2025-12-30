import csv
import os
import time
from tabulate import tabulate


File_path_csv = 'diem_clean.csv'

def danh_gia(TX,GK,CK):
    TB = round( TX * 0.1 + GK * 0.3 + CK * 0.6,2)
    if TB >= 8.5: 
        GPA = 4.0
        HL = 'Xuất sắc'
    elif TB >= 8.0: 
        GPA = 3.5
        HL = 'Khá giỏi'
    elif TB >= 7.0: 
        GPA = 3.0
        HL = "Khá"
    elif TB >= 6.5: 
        GPA = 2.5
        HL = 'Trung bình khá'
    elif TB >= 5.5: 
        GPA = 2.0
        HL = 'Trung bình'
    elif TB >= 5.0:
        GPA = 1.5
        HL = 'Trung bình yếu'
    elif TB >= 4.0:
        GPA = 1.0
        HL = 'Yếu'
    else: 
        GPA = 0.0
        HL = 'Kém'
    return (TB, GPA, HL)

class Lop_hoc:
    def __init__(self,msv, student, birth, thuong_xuyen, giua_ki, cuoi_ki):
        self.msv = msv
        self.ho_va_ten = student
        self.birth = birth
        self.thuong_xuyen = thuong_xuyen
        self.giua_ki = giua_ki
        self.cuoi_ki = cuoi_ki
        self.tong_diem, self.gpa, self.rank = danh_gia(float(self.thuong_xuyen), float(self.giua_ki), float(self.cuoi_ki))
    
data_hoc_sinh = {} ####### DATA QUAN TRỌNG ********* 
with open(File_path_csv, mode = 'r', encoding = 'utf-8-sig') as file:
    reader = csv.DictReader(file)
    for row in reader:
        hs = Lop_hoc(row['Mã SV'], row['Họ và tên'], row["Ngày sinh"], row['Điểm thường xuyên'], row['Điểm giữa kì'], row["Điểm cuối kì"])
        data_hoc_sinh[row['Mã SV']] = hs

class Admin:
    def them_hoc_sinh(self):
        while True:
            try:
                print("=== Thêm học sinh mới ===")
                id = int(input("Mã SV: "))
                name = (input("Họ và tên: "))
                birth_day = input("Nhập ngày tháng năm sinh:(theo cách nhau bằng /) ")
                tx = float(input("Điểm thường xuyên: "))
                gk = float(input("Điểm giữa kì: "))
                ck = float(input("Điểm cuối kì: "))
                confirm = input(("--- Bạn có chắc chắn với thao tác thêm học sinh hay không?(y = yes, n = no ): "))
                if confirm.lower() == 'y':
                    time.sleep(1)
                    if str(id) in data_hoc_sinh:
                        print("Đã tồn tại MÃ SINH VIÊN")
                    else:
                        print('---Thêm học sinh thành công---')
                        new_hoc_sinh = Lop_hoc(str(id), name,birth_day, tx , gk, ck)
                        data_hoc_sinh[f'{id}'] = new_hoc_sinh
                        with open(File_path_csv, mode = 'a',encoding = 'utf-8-sig', newline = '') as file:
                            writer = csv.writer(file)
                            writer.writerow([id, name ,'QH-2025-I/CQ-I-CS4',birth_day, tx, gk,ck])
                        return 
                elif confirm.lower() == 'n':
                    print("--- Đang thoát chương trình ...")
                    time.sleep(1)
                    return
            except (ValueError, TypeError):
                print("Định dạng không phù hợp!")

    def tim_kiem_hoc_sinh(self, msv):
        msv = str(msv) # Đảm bảo mã sinh viên là chuỗi để so sánh
        
        if msv in data_hoc_sinh:
            hs = data_hoc_sinh[msv]
            # Tính toán lại điểm tổng kết để hiển thị
            msvien, name , tx, gk, ck = data_hoc_sinh[msv].msv, data_hoc_sinh[msv].ho_va_ten, data_hoc_sinh[msv].thuong_xuyen, data_hoc_sinh[msv].giua_ki, data_hoc_sinh[msv].cuoi_ki
            tong_diem, gpa , rank = danh_gia(float(tx),float(gk), float(ck))
            # Tạo dữ liệu cho bảng (1 dòng duy nhất chứa thông tin hs đó)
            table_data = [[
                msvien,
                name,
                tx, 
                gk, 
                ck, 
                tong_diem, 
                gpa, 
                gpa, 
                rank
            ]]
            
            # Tạo tiêu đề cột
            headers = ["Mã SV", "Họ và tên", "Ngày sinh", "Điểm TX", "Điểm GK", "Điểm CK", "TB", "GPA", "Xếp loại"]
            
            print("\n" + "="*30 + " KẾT QUẢ TÌM KIẾM " + "="*30)
            # In ra dạng bảng lưới (grid) cho dễ nhìn
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
            
            input("\nẤn Enter để tiếp tục...")
        else:
            print(f"Không tìm thấy học sinh có mã số: {msv}")
            time.sleep(1)

    def thay_doi_diem(self, msv):
        if str(msv) in data_hoc_sinh:
            print("--- Lựa chọn thay đổi của bạn---")
            print('1. Họ và tên')
            print('2. Điểm thường xuyên')
            print('3. Điểm giữa kì')
            print('4. Điểm cuối kì')
            lst_input = list(map(int, input("Nhập lựa chọn của bạn cách nhau bới dấu cách: ").split()))
            lst_input = list(set(lst_input)) # để tránh trường hợp người dùng nhâp 1 1 1 1 
            try:
                for i in range(len(lst_input)):
                    if lst_input[i] == 1:
                        new_name = input("Nhập vào tên mới: ")
                        data_hoc_sinh[str(msv)].ho_va_ten = new_name
                        time.sleep(0.5)
                        print("--Thành công--")
                    elif lst_input[i] == 2:
                        new_tx = float(input("Nhập điểm thường xuyên mới: "))
                        data_hoc_sinh[str(msv)].thuong_xuyen = new_tx
                        time.sleep(0.5)
                        print("--Thành công--")
                    elif lst_input[i] == 3:
                        new_gk = float(input("Nhập điểm giữa kì mới: "))
                        data_hoc_sinh[str(msv)].giua_ki = new_gk
                        time.sleep(0.5)
                        print("--Thành công--")
                    elif lst_input[i] == 4:
                        new_ck = float(input("Nhập điểm cuối kì mới: "))
                        data_hoc_sinh[str(msv)].cuoi_ki = new_ck
                    else:
                        print("Không đúng định dạng")
                        time.sleep(0.5)
                        continue
                with open(File_path_csv, mode = 'w', encoding = 'utf-8-sig', newline='') as file:
                    fieldnames = ['Mã SV', 'Họ và tên', 'Ngày sinh', 'Điểm thường xuyên', 'Điểm giữa kì', 'Điểm cuối kì']
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    # 2. Ghi dòng tiêu đề đầu tiên
                    writer.writeheader()
                    for msvien, hsinh in data_hoc_sinh.items():
                        writer.writerow({
                            'Mã SV': hsinh.msv,
                            'Họ và tên': hsinh.ho_va_ten,
                            'Ngày sinh': hsinh.birth,
                            'Điểm thường xuyên' : hsinh.thuong_xuyen,
                            'Điểm giữa kì': hsinh.giua_ki,
                            'Điểm cuối kì': hsinh.cuoi_ki
                        })
            except (ValueError, TypeError):
                print("Định dạng bạn nhập không phù hợp!")
        else:
            print("Không tìm thấy học sinh")

def hien_thi_bang_diem():
    global data_hoc_sinh
    table_data = []
    for hs in data_hoc_sinh.values():
        avr, gpa , rank = danh_gia(float(hs.thuong_xuyen),float(hs.giua_ki), float(hs.cuoi_ki))
        table_data.append([
            hs.msv, 
            hs.ho_va_ten, 
            hs.birth, 
            hs.thuong_xuyen, 
            hs.giua_ki, 
            hs.cuoi_ki,
            avr,
            gpa,
            rank
        ])
    headers = ["Mã SV", "Họ và tên", "Ngày sinh", "Điểm TX", "Điểm GK", "Điểm CK",'Tổng Điểm', "GPA", "Đánh giá"]

    # In bảng với định dạng 'grid'
    print("\n" + "="*30 + " BẢNG ĐIỂM HỌC SINH " + "="*30)
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

def clear_screen():
    # Kiểm tra hệ điều hành để dùng lệnh xóa màn hình phù hợp
    os.system('cls' if os.name == 'nt' else 'clear')
def login():
    while True:
        clear_screen()
        print("CS4 - Quản lý điểm sinh viên")
        print("--------------------------")
        print("===== ĐĂNG NHẬP =====")
        account = input("Nhập account (nếu là sinh viên thì nhập mã sinh viên): ")
        if account == 'Patemuonnam':
            return Truy_cap_admin()

        else:
            if account in data_hoc_sinh:
                return Truy_cap_hoc_sinh(account)
            else:
                print("Không tìm thấy học sinh!")
                time.sleep(1)

def Truy_cap_admin():
    admin = Admin()
    while True:
        print("\n=== Phần mềm quản lý lớp học ===")
        print("1. Thêm học sinh mới")
        print("2. Tìm kiếm theo ID")
        print("3. Hiển thị tất cả điểm số")
        print("4. Sửa điểm")
        print("5. Thoát chương trình")
        choice = int(input("Nhập yêu cầu của bạn tương ứng với số: "))
        if choice == 1:
            admin.them_hoc_sinh()
        elif choice == 2:
            try:
                msv = input("Nhập mã sinh viên: ")
                admin.tim_kiem_hoc_sinh(msv)
            except (ValueError, TypeError):
                print("Định dạng không đúng!")
                time.sleep(0.5)
        elif choice == 3:
            hien_thi_bang_diem()
        elif choice == 4:
            try:
                msv = int(input("Nhập mã sinh viên: "))
                admin.thay_doi_diem(msv)
            except (ValueError, TypeError):
                print("Định dạng không đúng!")
                time.sleep(0.5)
        elif choice == 5:
            print("Quiting ...")
            time.sleep(1)
            break
        else:
            print("Vui lòng nhập lại!")
            time.sleep(0.5)
def Truy_cap_hoc_sinh(msv):
    hoc_sinh = Admin()
    while True:
        print("\n=== Phần mềm quản lý lớp học ===")
        print("1. Bảng điểm của lớp")
        print("2. Điểm của bản thân")
        print("3.Thoát chương trình")
        choice = int(input("Lựa chọn của bạn: "))
        if choice == 1:
            hien_thi_bang_diem()
        elif choice == 2:
            hoc_sinh.tim_kiem_hoc_sinh(msv)
        elif choice == 3:
            print("Quiting ...")
            time.sleep(1)
            break
        else:
            print("Vui lòng nhập lại!")
            time.sleep(0.5)
            break

if __name__ == "__main__":
    login()

        
            