from abc import ABC, abstractmethod

class Companion(ABC):
    """
    Khuôn mẫu chung (ABC) cho mọi sinh vật đồng hành.
    Sử dụng **kwargs để hỗ trợ Đa kế thừa hợp tác (Cooperative Multiple Inheritance).
    """
    def __init__(self, name: str, level: int = 1, **kwargs):
        super().__init__(**kwargs)  # Đẩy kwargs tiếp theo lên chuỗi MRO
        self.name = name
        self.level = level

    @abstractmethod
    def unleash_skill(self):
        """Kỹ năng đặc trưng buộc phải định nghĩa ở lớp con."""
        pass

    def __add__(self, other):
        """
        Nạp chồng toán tử cộng (+) để lai tạo sinh vật.
        Xử lý Bẫy 2: Ngăn chặn dị giáo lai tạo.
        """
        if type(self) is not type(other):
            raise TypeError("Chỉ có thể lai tạo 2 sinh vật cùng loài!")

        new_name = f"{self.name} {other.name}"
        new_level = self.level + 1

        kwargs = {'name': new_name, 'level': new_level}
        
        if hasattr(self, 'bonus_atk') and hasattr(other, 'bonus_atk'):
            kwargs['bonus_atk'] = self.bonus_atk + other.bonus_atk
            
        if hasattr(self, 'bonus_speed') and hasattr(other, 'bonus_speed'):
            kwargs['bonus_speed'] = self.bonus_speed + other.bonus_speed

        return type(self)(**kwargs)


class Pet(Companion):
    """Lớp Thú cưng - Hỗ trợ chiến đấu"""
    def __init__(self, bonus_atk: int = 0, **kwargs):
        super().__init__(**kwargs)
        self.bonus_atk = bonus_atk

    def unleash_skill(self):
        print(f">> {self.name} gầm gừ: Tấn công kẻ thù, gây {self.bonus_atk} sát thương!")


class Mount(Companion):
    """Lớp Thú cưỡi - Hỗ trợ di chuyển"""
    def __init__(self, bonus_speed: int = 0, **kwargs):
        super().__init__(**kwargs)
        self.bonus_speed = bonus_speed

    def unleash_skill(self):
        print(f">> {self.name} hí vang: Tăng tốc độ di chuyển thêm {self.bonus_speed} điểm!")


class Dragon(Pet, Mount):
    """
    Lớp Rồng Thần - Sinh vật thượng cổ đa kế thừa từ Pet và Mount.
    Nhờ kiến trúc **kwargs và super() ở các lớp cha, Bẫy 3 (Nút thắt MRO) đã được gỡ bỏ.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def unleash_skill(self):
        print(f">> {self.name} thị uy:")
        print(f"   - Tấn công kẻ thù, gây {self.bonus_atk} sát thương!")
        print(f"   - Tăng tốc độ di chuyển thêm {self.bonus_speed} điểm!")


def display_team(active_companions: list):
    """Chức năng 1: Xem đội hình sinh vật"""
    print("--- ĐỘI HÌNH SINH VẬT ---")
    if not active_companions:
        print("Đội hình đang trống!")
        return
        
    for i, comp in enumerate(active_companions, 1):
        loai = comp.__class__.__name__
        if loai == "Dragon":
            print(f"{i}. [{loai}] {comp.name} | Cấp: {comp.level} | Atk: +{comp.bonus_atk} | Speed: +{comp.bonus_speed}")
        elif loai == "Pet":
            print(f"{i}. [{loai}] {comp.name} | Cấp: {comp.level} | Atk: +{comp.bonus_atk}")
        elif loai == "Mount":
            print(f"{i}. [{loai}] {comp.name} | Cấp: {comp.level} | Speed: +{comp.bonus_speed}")

def summon_companion(active_companions: list):
    """Chức năng 2 & 3: Triệu hồi sinh vật"""
    print("\n--- TRIỆU HỒI SINH VẬT ---")
    print("1. Thú cưng (Pet)\n2. Thú cưỡi (Mount)\n3. Rồng Thần (Dragon)")
    choice = input("Chọn loại sinh vật (1-3): ")
    
    if choice not in ['1', '2', '3']:
        print("Lựa chọn không hợp lệ!")
        return
        
    name = input("Nhập tên sinh vật: ").strip()
    
    try:
        if choice == '1':
            atk = int(input("Nhập sức mạnh cộng thêm (bonus_atk): "))
            active_companions.append(Pet(name=name, bonus_atk=atk))
        elif choice == '2':
            speed = int(input("Nhập tốc độ cộng thêm (bonus_speed): "))
            active_companions.append(Mount(name=name, bonus_speed=speed))
        elif choice == '3':
            atk = int(input("Nhập sức mạnh cộng thêm (bonus_atk): "))
            speed = int(input("Nhập tốc độ cộng thêm (bonus_speed): "))
            active_companions.append(Dragon(name=name, bonus_atk=atk, bonus_speed=speed))
            
        print(f">> Triệu hồi [{name}] thành công!")
    except ValueError:
        print(">> Lỗi: Chỉ số phải là một số nguyên!")

def breed_companions(active_companions: list):
    """Chức năng 4: Lai tạo sinh vật"""
    print("--- LAI TẠO SINH VẬT ---")
    display_team(active_companions)
    if len(active_companions) < 2:
        print("Cần ít nhất 2 sinh vật trong đội hình để lai tạo!")
        return
        
    try:
        idx1 = int(input("Chọn sinh vật 1 (nhập STT): ")) - 1
        idx2 = int(input("Chọn sinh vật 2 (nhập STT): ")) - 1
        
        c1 = active_companions[idx1]
        c2 = active_companions[idx2]
        
        new_beast = c1 + c2  
        active_companions.append(new_beast)
        
        chi_so = f"Atk: {getattr(new_beast, 'bonus_atk', 0)}" if isinstance(new_beast, Pet) else f"Speed: {getattr(new_beast, 'bonus_speed', 0)}"
        if isinstance(new_beast, Dragon):
            chi_so = f"Atk: {new_beast.bonus_atk}, Speed: {new_beast.bonus_speed}"
            
        print(f">> Lai tạo thành công! Nhận được: {new_beast.name} (Cấp {new_beast.level}, {chi_so})")
        
    except (ValueError, IndexError):
        print(">> Lỗi: STT không hợp lệ!")
    except TypeError as e:
        print(f">> Lỗi Lai Tạo: {e}")

def combat(active_companions: list):
    """Chức năng 5: Xuất chiến (Polymorphism)"""
    print("--- XUẤT CHIẾN ---")
    if not active_companions:
        print("Đội hình đang trống!")
        return
        
    for comp in active_companions:
        comp.unleash_skill()


def main():
    active_companions = []
    
    active_companions.append(Pet(name="Sói Trắng", bonus_atk=50))
    active_companions.append(Mount(name="Hắc Mã", bonus_speed=20))
    
    while True:
        print("="*40)
        print("RIKKEI RPG - HỆ THỐNG BẠN ĐỒNG HÀNH")
        print("="*40)
        print("1. Xem đội hình sinh vật")
        print("2. Triệu hồi sinh vật")
        print("3. Lai tạo sinh vật")
        print("4. Xuất chiến")
        print("5. Thoát game")
        
        choice = input("\nChọn chức năng (1-5): ")
        
        if choice == '1':
            display_team(active_companions)
        elif choice == '2':
            summon_companion(active_companions)
        elif choice == '3':
            breed_companions(active_companions)
        elif choice == '4':
            combat(active_companions)
        elif choice == '5':
            print("Đã thoát hệ thống Bạn Đồng Hành!")
            break
        else:
            print("Lựa chọn không hợp lệ, vui lòng chọn lại!")

if __name__ == "__main__":
    main()