from abc import ABC, abstractmethod

class Equipment(ABC):
    """Lớp trừu tượng cơ sở (Abstract Base Class)"""
    @abstractmethod
    def calculate_total_damage(self):
        pass

class Weapon(Equipment):
    """Lớp Vũ khí vật lý"""
    def __init__(self, name: str, base_damage: int, upgrade_level: int = 0):
        self.name = name
        self.base_damage = base_damage
        self.upgrade_level = upgrade_level

    def calculate_total_damage(self) -> int:
        return self.base_damage + (self.upgrade_level * 10)

    def __gt__(self, other):
        if not isinstance(other, Equipment):
            print("Chỉ có thể dung hợp/so sánh giữa các trang bị!")
            return False
        return self.calculate_total_damage() > other.calculate_total_damage()

    def __add__(self, other):
        if not isinstance(other, Equipment):
            print("Chỉ có thể dung hợp/so sánh giữa các trang bị!")
            return None
        new_upgrade = self.upgrade_level + other.upgrade_level
        return Weapon(self.name, self.base_damage, new_upgrade)

class MagicMixin:
    """Lớp hỗ trợ (Mixin) cung cấp thuộc tính phép thuật"""
    def __init__(self, magic_power: int):
        self.magic_power = magic_power

    def cast_glow(self):
        print(f"[{self.name}] đang phát sáng rực rỡ!")

class MagicSword(Weapon, MagicMixin):
    """Lớp Kiếm Ma Thuật (Multiple Inheritance)"""
    def __init__(self, name: str, base_damage: int, upgrade_level: int, magic_power: int):
        # Bẫy 3: Khởi tạo đích danh các lớp cha để tránh MRO bỏ sót thuộc tính
        Weapon.__init__(self, name, base_damage, upgrade_level)
        MagicMixin.__init__(self, magic_power)

    def calculate_total_damage(self) -> int:
        return super().calculate_total_damage() + self.magic_power



def display_inventory(inventory: list):
    """Chức năng 1: Xem kho vũ khí"""
    print("\n--- KHO VŨ KHÍ CỦA NGƯỜI CHƠI ---")
    if not inventory:
        print("Kho vũ khí hiện đang trống.")
        print("Vui lòng rèn vũ khí bằng Chức năng 2 hoặc Chức năng 3.")
        return
        
    print(f"{'STT':<5} | {'Tên vũ khí':<20} | {'Loại':<12} | {'Cấp':<5} | {'Sát thương tổng'}")
    print("-" * 70)
    for i, item in enumerate(inventory, 1):
        loai = "MagicSword" if isinstance(item, MagicSword) else "Weapon"
        print(f"{i:<5} | {item.name.title():<20} | {loai:<12} | {item.upgrade_level:<5} | {item.calculate_total_damage()}")

def forge_weapon(inventory: list):
    """Chức năng 2: Rèn Vũ khí Vật lý"""
    print("--- RÈN VŨ KHÍ VẬT LÝ ---")
    name = input("Nhập tên vũ khí: ").strip()
    
    base_damage = int(input("Nhập sát thương gốc: "))
    if base_damage <= 0:
        print("Giá trị phải lớn hơn 0!")
        return
        
    upgrade_level = int(input("Nhập cấp cường hóa: "))
    if upgrade_level <= 0:
        print("Giá trị phải lớn hơn 0!")
        return

    w = Weapon(name.title(), base_damage, upgrade_level)
    inventory.append(w)
    
    print(">> Rèn vũ khí vật lý thành công!")
    print(f"Tên vũ khí: {w.name}\nLoại: Weapon\nCấp cường hóa: {w.upgrade_level}\nSát thương tổng: {w.calculate_total_damage()}")

def forge_magic_sword(inventory: list):
    """Chức năng 3: Rèn Kiếm Ma Thuật"""
    print("--- RÈN KIẾM MA THUẬT ---")
    name = input("Nhập tên kiếm ma thuật: ").strip()
    
    base_damage = int(input("Nhập sát thương gốc: "))
    if base_damage <= 0:
        print("Giá trị phải lớn hơn 0!")
        return
        
    upgrade_level = int(input("Nhập cấp cường hóa: "))
    if upgrade_level <= 0:
        print("Giá trị phải lớn hơn 0!")
        return
        
    magic_power = int(input("Nhập sức mạnh phép thuật: "))
    if magic_power <= 0:
        print("Giá trị phải lớn hơn 0!")
        return

    ms = MagicSword(name.title(), base_damage, upgrade_level, magic_power)
    inventory.append(ms)
    
    print(">> Rèn kiếm ma thuật thành công!")
    print(f"Tên vũ khí: {ms.name}\nLoại: MagicSword\nCấp cường hóa: {ms.upgrade_level}")
    print(f"Sát thương gốc: {ms.base_damage}\nSức mạnh phép thuật: {ms.magic_power}\nSát thương tổng: {ms.calculate_total_damage()}")

def appraise_weapons(inventory: list):
    """Chức năng 4: Thẩm định (Sử dụng __gt__)"""
    print("--- THẨM ĐỊNH VŨ KHÍ ---")
    if len(inventory) < 2:
        print("Cần ít nhất 2 vũ khí trong kho để thẩm định!")
        return
        
    w1, w2 = inventory[0], inventory[1]
    l1 = "MagicSword" if isinstance(w1, MagicSword) else "Weapon"
    l2 = "MagicSword" if isinstance(w2, MagicSword) else "Weapon"
    
    print("Vũ khí thứ nhất:")
    print(f"{w1.name} | Loại: {l1} | Sát thương: {w1.calculate_total_damage()}")
    print("Vũ khí thứ hai:")
    print(f"{w2.name} | Loại: {l2} | Sát thương: {w2.calculate_total_damage()}")
    
    print("Kết quả: ", end="")
    if w1 > w2:
        print(f"{w1.name} mạnh hơn {w2.name}.")
    elif w2 > w1:
        print(f"{w2.name} mạnh hơn {w1.name}.")
    else:
        print("Hai vũ khí có sức mạnh ngang nhau.")

def fuse_weapons(inventory: list):
    """Chức năng 5: Dung hợp (Sử dụng __add__)"""
    print("--- DUNG HỢP VŨ KHÍ ---")
    if len(inventory) < 2:
        print("Cần ít nhất 2 vũ khí trong kho để dung hợp!")
        return
        
    w1, w2 = inventory[0], inventory[1]
    
    new_weapon = w1 + w2  
    
    if new_weapon:
        inventory.pop(0)
        inventory.pop(0)
        inventory.append(new_weapon)
        print(f"Dung hợp thành công! Món đồ mới: {new_weapon.name} | Cấp: {new_weapon.upgrade_level}")


def main():
    
    inventory = []
    
    while True:
        print(+ "="*5 + " LÒ RÈN VŨ KHÍ RIKKEI STUDIOS " + "="*5)
        print("1. Xem kho vũ khí & Sát thương tổng")
        print("2. Rèn Vũ khí Vật lý (Tạo Weapon)")
        print("3. Rèn Kiếm Ma Thuật (Tạo MagicSword)")
        print("4. Thẩm định vũ khí (So sánh lớn hơn)")
        print("5. Dung hợp vũ khí (Cộng dồn cấp độ)")
        print("6. Thoát game")
        print("=" * 40)
        
        try:
            choice = int(input("Chọn chức năng (1-6): "))
        except ValueError:
            print("Vui lòng nhập một số nguyên!")
            continue
            
        if choice == 1:
            display_inventory(inventory)
        elif choice == 2:
            forge_weapon(inventory)
        elif choice == 3:
            forge_magic_sword(inventory)
        elif choice == 4:
            appraise_weapons(inventory)
        elif choice == 5:
            fuse_weapons(inventory)
        elif choice == 6:
            print("Thoát Lò Rèn. Hẹn gặp lại Anh hùng!")
            break
        else:
            print("Lựa chọn không hợp lệ, vui lòng chọn từ 1-6.")

if __name__ == "__main__":
    main()