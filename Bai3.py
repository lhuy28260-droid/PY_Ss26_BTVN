from abc import ABC, abstractmethod

class Champion(ABC):
    """
    Lớp cơ sở trừu tượng (Abstract Base Class) đại diện cho một quân cờ.
    Không thể khởi tạo trực tiếp lớp này.
    """
    def __init__(self, champion_id: str, name: str, base_hp: int, base_atk: int):
        self.champion_id = champion_id
        self.name = name
        
        # Bẫy 2: Xử lý chỉ số âm hoặc bằng 0
        self.base_hp = base_hp if base_hp > 0 else 100
        self.base_atk = base_atk if base_atk > 0 else 100

    @abstractmethod
    def calculate_skill_damage(self) -> float:
        """Phương thức trừu tượng bắt buộc các lớp con phải ghi đè để tính sát thương kĩ năng."""
        pass

    def get_combat_power(self) -> float:
        """Tính điểm chiến lực tổng hợp: Máu + {Sát thương kỹ năng} * 1.5"""
        return self.base_hp + (self.calculate_skill_damage() * 1.5)

    def __add__(self, other):
        """Nạp chồng toán tử + để cộng dồn điểm chiến lực giữa các quân cờ hoặc với một số."""
        if isinstance(other, (int, float)):
            return self.get_combat_power() + other
        elif isinstance(other, Champion):
            return self.get_combat_power() + other.get_combat_power()
        return NotImplemented

    def __radd__(self, other):
        """Hỗ trợ toán tử cộng tích lũy đảo chiều (phục vụ vòng lặp cộng dồn từ số 0)."""
        return self.__add__(other)

    def __gt__(self, other):
        """Nạp chồng toán tử > để so sánh điểm chiến lực giữa 2 quân cờ."""
        if isinstance(other, Champion):
            return self.get_combat_power() > other.get_combat_power()
        return NotImplemented


class Warrior(Champion):
    """Lớp cụ thể (Concrete Class) đại diện cho hệ Chiến binh."""
    def __init__(self, champion_id: str, name: str, base_hp: int, base_atk: int, shield_bonus: int):
        super().__init__(champion_id, name, base_hp, base_atk)
        self.shield_bonus = shield_bonus if shield_bonus >= 0 else 0

    def calculate_skill_damage(self) -> float:
        """Ghi đè: Sát thương kỹ năng = base_atk * 2 + shield_bonus"""
        return self.base_atk * 2 + self.shield_bonus


class Mage(Champion):
    """Lớp cụ thể (Concrete Class) đại diện cho hệ Pháp sư."""
    def __init__(self, champion_id: str, name: str, base_hp: int, base_atk: int, ability_power: float):
        super().__init__(champion_id, name, base_hp, base_atk)
        self.ability_power = ability_power if ability_power > 0 else 1.0

    def calculate_skill_damage(self) -> float:
        """Ghi đè: Sát thương kỹ năng = base_atk * ability_power"""
        return self.base_atk * self.ability_power


def input_int(prompt: str) -> int:
    """Ép kiểu dữ liệu an toàn cho số nguyên."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Lỗi hệ thống: Vui lòng nhập vào một số nguyên hợp lệ!")

def input_float(prompt: str) -> float:
    """Ép kiểu dữ liệu an toàn cho số thực."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Lỗi hệ thống: Vui lòng nhập vào một số thực hợp lệ!")


def display_pool(champion_pool: dict):
    """Chức năng 1: Hiển thị bể tướng hiện có dưới dạng bảng chuẩn hóa."""
    print("\n--- DANH SÁCH QUÂN CỜ TRONG BỂ TƯỚNG ---")
    print(f"{'Mã':<6} | {'Tên tướng':<18} | {'Hệ':<9} | {'HP':<5} | {'ATK':<5} | {'Chỉ số riêng':<15} | {'Chiến lực'}")
    print("-" * 80)
    for cid, champ in champion_pool.items():
        he_toc = "Warrior" if isinstance(champ, Warrior) else "Mage"
        cho_so_rieng = f"Armor: {champ.shield_bonus}" if isinstance(champ, Warrior) else f"Mana/AP: {champ.ability_power}"
        print(f"{champ.champion_id:<6} | {champ.name:<18} | {he_toc:<9} | {champ.base_hp:<5} | {champ.base_atk:<5} | {cho_so_rieng:<15} | {champ.get_combat_power():.0f}")

def add_champion(champion_pool: dict):
    """Chức năng 2: Thêm quân cờ mới vào hệ thống bể tướng."""
    print("--- TẠO TƯỚNG MỚI ---")
    print("Chọn Hệ (1 - Warrior, 2 - Mage)")
    choice = input_int("Lựa chọn của bạn: ")
    if choice not in [1, 2]:
        print("Lựa chọn hệ không hợp lệ! Hủy tác vụ.")
        return

    cid = input("Nhập mã tướng: ").strip().upper()
    
    if cid in champion_pool:
        print(f"Lỗi: Mã tướng [{cid}] đã tồn tại trong bể tướng! Từ chối thêm mới.")
        return

    name = input("Nhập tên tướng: ").strip()
    hp = input_int("Nhập HP: ")
    atk = input_int("Nhập ATK: ")

    if choice == 1:
        armor = input_int("Nhập Armor: ")
        new_champ = Warrior(cid, name, hp, atk, armor)
    else:
        ap = input_float("Nhập Ability Power (Hệ số phép): ")
        new_champ = Mage(cid, name, hp, atk, ap)

    champion_pool[cid] = new_champ
    print(f"Thêm tướng {'Warrior' if choice==1 else 'Mage'} thành công!")
    print(f"Mã: {new_champ.champion_id} | Tên: {new_champ.name} | Chiến lực: {new_champ.get_combat_power():.0f}")

def compare_champions(champion_pool: dict):
    """Chức năng 3: So sánh sức mạnh chiến lực giữa 2 quân cờ sử dụng toán tử >."""
    print("\n--- SO SÁNH SỨC MẠNH 2 QUÂN CỜ ---")
    cid1 = input("Nhập mã tướng thứ nhất: ").strip().upper()
    cid2 = input("Nhập mã tướng thứ hai: ").strip().upper()

    if cid1 not in champion_pool:
        print(f"Mã tướng [{cid1}] không hợp lệ, bỏ qua!")
        return
    if cid2 not in champion_pool:
        print(f"Mã tướng [{cid2}] không hợp lệ, bỏ qua!")
        return

    c1 = champion_pool[cid1]
    c2 = champion_pool[cid2]

    print("Thông tin so sánh:")
    for c in [c1, c2]:
        he = "Warrior" if isinstance(c, Warrior) else "Mage"
        print(f"{c.champion_id} - {c.name} | Hệ: {he} | Chiến lực: {c.get_combat_power():.0f}")

    if c1 > c2:
        print(f"Kết quả: {c1.champion_id} - {c1.name} mạnh hơn {c2.champion_id} - {c2.name}.")
    elif c2 > c1:
        print(f"Kết quả: {c2.champion_id} - {c2.name} mạnh hơn {c1.champion_id} - {c1.name}.")
    else:
        print(f"Kết quả: Hai quân cờ có chiến lực ngang nhau.")

def calculate_team_power(champion_pool: dict):
    """Chức năng 4: Tính tổng điểm chiến lực của đội hình ra sân bằng toán tử +."""
    print("--- TÍNH TỔNG CHIẾN LỰC ĐỘI HÌNH RA SÂN ---")
    raw_input = input("Nhập danh sách mã tướng, cách nhau bằng dấu phẩy (Ví dụ: WAR01, MAG01): ")
    selected_ids = [cid.strip().upper() for cid in raw_input.split(",") if cid.strip()]

    team_champions = []
    print("Danh sách đội hình:")
    count = 1
    for cid in selected_ids:
        if cid not in champion_pool:
            print(f"Mã tướng [{cid}] không hợp lệ, bỏ qua!")
            continue
        
        champ = champion_pool[cid]
        team_champions.append(champ)
        print(f"{count}. {champ.champion_id} - {champ.name} | Chiến lực: {champ.get_combat_power():.0f}")
        count += 1

    if not team_champions:
        print("Đội hình trống hoặc không có tướng nào hợp lệ!")
        return

    total_power = sum(team_champions)
    print(f"Tổng chiến lực đội hình: {total_power:.0f}")


def main():
    champion_pool = {
        "WAR01": Warrior("WAR01", "Rikkei Knight", 1200, 300, 150),
        "WAR02": Warrior("WAR02", "Steel Guardian", 1500, 250, 200),
        "MAG01": Mage("MAG01", "Rikkei Wizard", 800, 500, 2.0)
    }

    try:
        abstract_test = Champion("TEST", "Error Champ", 100, 100)
    except TypeError:
        pass

    while True:
        print("\n" + "="*40)
        print("RIKKEI RPG - AUTO-BATTLER MANAGER")
        print("="*40)
        print("1. Hiển thị bể tướng hiện có")
        print("2. Thêm quân cờ mới")
        print("3. So sánh 2 quân cờ")
        print("4. Tính tổng chiến lực Đội hình ra sân")
        print("5. Thoát chương trình")
        
        choice = input_int("\nChọn chức năng (1-5): ")
        
        if choice == 1:
            display_pool(champion_pool)
        elif choice == 2:
            add_champion(champion_pool)
        elif choice == 3:
            compare_champions(champion_pool)
        elif choice == 4:
            calculate_team_power(champion_pool)
        elif choice == 5:
            print("Cảm ơn bạn đã sử dụng Rikkei RPG - Auto-Battler Manager!")
            break
        else:
            print("Lựa chọn không nằm trong danh mục (1-5), vui lòng nhập lại!")

if __name__ == "__main__":
    main()