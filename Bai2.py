from abc import ABC, abstractmethod

# Lớp cha: Khuôn mẫu Tướng sử dụng thư viện ABC
class Hero(ABC):
    @abstractmethod
    def use_ultimate(self):
        pass

# Lớp con 1: Pháp Sư
class Mage(Hero):
    def use_ultimate(self):
        print("🔥 Pháp Sư tung chiêu: MƯA SAO BĂNG!")

# Lớp con 2: Sát Thủ (Đã sửa đổi tên hàm cho đúng khuôn mẫu)
class Assassin(Hero):
    def use_ultimate(self):
        print("🗡️ Sát Thủ tung chiêu: ÁM SÁT TỪ PHÍA SAU!")

# --- KỊCH BẢN MATCHMAKING (Đã an toàn) ---
print("--- LOADING TRẬN ĐẤU ---")
# Việc khởi tạo diễn ra an toàn. Nếu Assassin thiếu use_ultimate, 
# chương trình sẽ báo lỗi TypeError ngay tại dòng này.
team_heroes = [Mage(), Assassin()]
print("Tải trận đấu thành công! Các tướng đã sẵn sàng...\n")

print("--- GIAO TRANH TỔNG BẮT ĐẦU ---")
# Vòng lặp Đa hình (Polymorphism)
for hero in team_heroes:
    hero.use_ultimate()