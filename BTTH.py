from abc import ABC, abstractmethod


class Employee(ABC):
    """Lớp trừu tượng đại diện cho nhân viên."""
    def __init__(self, employee_id: str, name: str):
        self.employee_id = employee_id
        self.name = name

    @abstractmethod
    def display_info(self):
        """Hiển thị thông tin cơ bản. Lớp con phải ghi đè để có Type chuẩn."""
        pass

    @abstractmethod
    def calculate_salary(self) -> float:
        """Tính lương. Lớp con bắt buộc phải ghi đè."""
        pass

class FullTimeEmployee(Employee):
    """Nhân viên toàn thời gian"""
    def __init__(self, employee_id: str, name: str, base_salary: float, bonus: float):
        super().__init__(employee_id, name)
        self.base_salary = base_salary
        self.bonus = bonus

    def display_info(self):
        print(f"Mã NV: {self.employee_id} | Họ tên: {self.name} | Loại: Full-time")

    def calculate_salary(self) -> float:
        return self.base_salary + self.bonus

class PartTimeEmployee(Employee):
    """Nhân viên bán thời gian"""
    def __init__(self, employee_id: str, name: str, working_hours: float, hourly_rate: float):
        super().__init__(employee_id, name)
        self.working_hours = working_hours
        self.hourly_rate = hourly_rate
        
    def display_info(self):
        print(f"Mã NV: {self.employee_id} | Họ tên: {self.name} | Loại: Part-time")

    def calculate_salary(self) -> float:
        return self.working_hours * self.hourly_rate

class InternEmployee(Employee):
    """Thực tập sinh"""
    def __init__(self, employee_id: str, name: str, allowance: float):
        super().__init__(employee_id, name)
        self.allowance = allowance
        
    def display_info(self):
        print(f"Mã NV: {self.employee_id} | Họ tên: {self.name} | Loại: Intern")

    def calculate_salary(self) -> float:
        return self.allowance




def display_employees(employees: list):
    """Chức năng 1: Xem danh sách nhân viên"""
    print("\n--- DANH SÁCH NHÂN VIÊN ---")
    for emp in employees:
        emp.display_info()

def display_salaries(employees: list):
    """
    Chức năng 2: Tính lương toàn bộ nhân viên.
    Thể hiện rõ tính Đa hình (Polymorphism): Không sử dụng lệnh if/elif/match-case
    để kiểm tra kiểu dữ liệu, chỉ gọi chung method calculate_salary().
    """
    print("--- BẢNG LƯƠNG NHÂN VIÊN ---")
    for emp in employees:
        salary = emp.calculate_salary()
        # Định dạng có dấu phẩy ngăn cách hàng nghìn và đuôi VND
        print(f"{emp.employee_id} | {emp.name} | Lương: {salary:,.0f} VND")




def main():
    
    employees = [
        FullTimeEmployee("E001", "Nguyen Van A", 15000000, 3000000),
        PartTimeEmployee("E002", "Tran Thi B", 80, 50000),
        InternEmployee("E003", "Le Van C", 3000000)
    ]

    while True:
        print("\n=== EMPLOYEE SALARY MANAGER ===")
        print("1. Xem danh sách nhân viên")
        print("2. Tính lương toàn bộ nhân viên")
        print("3. Thoát chương trình")
        print("===============================")
        
        try:
            choice = int(input("Chọn chức năng (1-3): "))
            
            if choice == 1:
                display_employees(employees)
            elif choice == 2:
                display_salaries(employees)
            elif choice == 3:

                print("Cảm ơn bạn đã sử dụng Employee Salary Manager!")
                break
            else:
                print("Lựa chọn không hợp lệ. Vui lòng thử lại.")
                
        except ValueError:
            print("Lựa chọn không hợp lệ. Vui lòng thử lại.")

if __name__ == "__main__":
    main()