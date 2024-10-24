import streamlit as st
import pandas as pd
import requests
import csv
import matplotlib.pyplot as plt

# Hàm để lấy dữ liệu từ API
def get_team_data(team_id, tournament_id, season_id):
    url = f"https://sofascore.p.rapidapi.com/teams/get-player-statistics?teamId={team_id}&tournamentId={tournament_id}&seasonId={season_id}&type=overall"
    headers = {
        'x-rapidapi-host': 'sofascore.p.rapidapi.com',
        'x-rapidapi-key': '5fa1b3ec61msh748c83f0ec34ff4p18fe14jsn062670fd057e'  # Thay thế bằng API key của bạn
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to retrieve data: {response.status_code}")
        return None
# Gợi ý kèm theo URL logo
teams = {
    "Liverpool - 44": "https://api.sofascore.app/api/v1/team/44/image",
    "Manchester City - 17": "https://api.sofascore.app/api/v1/team/17/image",
    "Arsenal - 42": "https://api.sofascore.app/api/v1/team/42/image",
    "Chelsea - 38": "https://api.sofascore.app/api/v1/team/38/image",
    "Tottenham - 33": "https://api.sofascore.app/api/v1/team/33/image",
    "Manchester United - 35": "https://api.sofascore.app/api/v1/team/35/image",
    "Real Madrid - 2829": "https://api.sofascore.app/api/v1/team/2829/image",
    "Barcelona - 2817": "https://api.sofascore.app/api/v1/team/2817/image",
    "Alentico Madrid - 2836": "https://api.sofascore.app/api/v1/team/2836/image",
    "Bayern Munich - 2672": "https://api.sofascore.app/api/v1/team/2672/image",
    "Borussia Dortmund - 2673": "https://api.sofascore.app/api/v1/team/2673/image",
    "Bayern Leverkusen - 2681": "https://api.sofascore.app/api/v1/team/2681/image",
    "Juventus - 2687": "https://api.sofascore.app/api/v1/team/2687/image",
    "AC Milan - 2692": "https://api.sofascore.app/api/v1/team/2692/image",
    "Inter Milan - 2697": "https://api.sofascore.app/api/v1/team/2697/image",
    "Napoli - 2714": "https://api.sofascore.app/api/v1/team/2714/image",
    "Paris Saint-Germain - 1644": "https://api.sofascore.app/api/v1/team/1644/image",
    "Inter Miami - 337602": "https://api.sofascore.app/api/v1/team/337602/image",
    "Al Nass - 23400": "https://api.sofascore.app/api/v1/team/23400/image",
    "Al Hilal - 21895": "https://api.sofascore.app/api/v1/team/21895/image",
    "Al Ittihad - 34315": "https://api.sofascore.app/api/v1/team/34315/image",


}

tournaments = {
    "UEFA Champions League - 7": "https://api.sofascore.app/api/v1/unique-tournament/7/image/dark",
    "Premier League - 17": "https://api.sofascore.app/api/v1/unique-tournament/17/image/dark",
    "La Liga - 8": "https://api.sofascore.app/api/v1/unique-tournament/8/image/dark",
    "Bundesliga - 35": "https://api.sofascore.app/api/v1/unique-tournament/35/image/dark",
    "Serie A - 23": "https://api.sofascore.app/api/v1/unique-tournament/23/image/dark",
    "V-League - 626": "https://api.sofascore.app/api/v1/unique-tournament/626/image/dark",
    "mls - 242": "https://api.sofascore.app/api/v1/unique-tournament/242/image/dark",
    "saudi-professional-league - 955": "https://api.sofascore.app/api/v1/unique-tournament/955/image/dark",
}

seasons = {
    "UEFA Champions League 2024/2025 - 61644": "https://api.sofascore.app/api/v1/unique-tournament/7/image/dark",
    "UEFA Champions League 2023/2024 - 52162": "https://api.sofascore.app/api/v1/unique-tournament/7/image/dark",
    "UEFA Champions League 2022/2023 - 41897": "https://api.sofascore.app/api/v1/unique-tournament/7/image/dark",
    "UEFA Champions League 2021/2022 - 36886": "https://api.sofascore.app/api/v1/unique-tournament/7/image/dark",
    "UEFA Champions League 2020/2021 - 29267": "https://api.sofascore.app/api/v1/unique-tournament/7/image/dark",
    "Premier League 2024/2025 - 61627": "https://api.sofascore.app/api/v1/unique-tournament/17/image/dark",
    "Premier League 2023/2024 - 52186": "https://api.sofascore.app/api/v1/unique-tournament/17/image/dark",
    "Premier League 2022/2023 - 41886": "https://api.sofascore.app/api/v1/unique-tournament/17/image/dark",
    "Premier League 2021/2022 - 37036": "https://api.sofascore.app/api/v1/unique-tournament/17/image/dark",
    "Premier League 2020/2021 - 29415": "https://api.sofascore.app/api/v1/unique-tournament/17/image/dark",
    "La Liga 2024/2025 - 61643": "https://api.sofascore.app/api/v1/unique-tournament/8/image/dark",
    "La Liga 2023/2024 - 52376": "https://api.sofascore.app/api/v1/unique-tournament/8/image/dark",
    "La Liga 2022/2023 - 42409": "https://api.sofascore.app/api/v1/unique-tournament/8/image/dark",
    "La Liga 2021/2022 - 37223": "https://api.sofascore.app/api/v1/unique-tournament/8/image/dark",
    "La Liga 2020/2021 - 32501": "https://api.sofascore.app/api/v1/unique-tournament/8/image/dark",
    "Bundesliga 2024/2025 - 63516": "https://api.sofascore.app/api/v1/unique-tournament/35/image/dark",
    "Bundesliga 2023/2024 - 52608": "https://api.sofascore.app/api/v1/unique-tournament/35/image/dark",
    "Bundesliga 2022/2023 - 42268": "https://api.sofascore.app/api/v1/unique-tournament/35/image/dark",
    "Bundesliga 2021/2022 - 37166": "https://api.sofascore.app/api/v1/unique-tournament/35/image/dark",
    "Bundesliga 2020/2021 - 28210": "https://api.sofascore.app/api/v1/unique-tournament/35/image/dark",
    "Serie A 2024/2025 - 63515": "https://api.sofascore.app/api/v1/unique-tournament/23/image/dark",
    "Serie A 2023/2024 - 52760": "https://api.sofascore.app/api/v1/unique-tournament/23/image/dark",
    "Serie A 2022/2023 - 42415": "https://api.sofascore.app/api/v1/unique-tournament/23/image/dark",
    "Serie A 2021/2022 - 37475": "https://api.sofascore.app/api/v1/unique-tournament/23/image/dark",
    "Serie A 2020/2021 - 32523": "https://api.sofascore.app/api/v1/unique-tournament/23/image/dark",
    "Ligue 1 2024/2025 - 61736": "https://api.sofascore.app/api/v1/unique-tournament/34/image/dark",
    "Ligue 1 2023/2024 - 52571": "https://api.sofascore.app/api/v1/unique-tournament/34/image/dark",
    "Ligue 1 2022/2023 - 42273": "https://api.sofascore.app/api/v1/unique-tournament/34/image/dark",
    "Ligue 1 2021/2022 - 37167": "https://api.sofascore.app/api/v1/unique-tournament/34/image/dark",
    "Ligue 1 2020/2021 - 28222": "https://api.sofascore.app/api/v1/unique-tournament/34/image/dark",
    "Mls 2024/2025 - 57317": "https://api.sofascore.app/api/v1/unique-tournament/242/image/dark",
    "Saudi-professional-league 2024/2025 - 63998": "https://api.sofascore.app/api/v1/unique-tournament/955/image/dark",  
}

# Thiết lập giao diện
st.image('football_banner.jpeg', use_column_width=True)  # Ảnh banner bóng đá
st.title("⚽THỐNG KÊ DỮ LIỆU ĐỘI BÓNG⚽")

st.markdown("""
    **Chào mừng bạn đến với trang thống kê bóng đá!**
    Hãy nhập các thông tin cần thiết và chúng tôi sẽ lấy dữ liệu về đội bóng của bạn.
""")
st.markdown("""
    **Hướng dẫn:**
    - Mỗi tùy chọn bao gồm tên và ID, được phân cách bởi dấu " - ".
    - Ví dụ: Nếu bạn chọn "Liverpool - 44", thì ID của Liverpool là **44**.
    - ID này sẽ được sử dụng để truy xuất dữ liệu từ API.
    - Hãy chắc chắn rằng đội bóng của bạn ở đúng giải đấu và mùa giải bạn chọn.
""")

# Hiển thị gợi ý id đội bóng kèm logo và cho phép chọn
with st.expander("Gợi ý id đội bóng:"):
    team_options = []
    for team, logo_url in teams.items():
        col1, col2 = st.columns([1, 5])
        with col1:
            st.image(logo_url, width=50)
        with col2:
            st.markdown(team)
        team_options.append(team)
    st.markdown("<h4 style='color: #0072B8;'>Chọn đội bóng:</h4>", unsafe_allow_html=True)  # Tiêu đề nổi bật
    selected_team = st.selectbox("🟢 Chọn đội bóng", team_options, index=0)  # Thêm biểu tượng

# Hiển thị gợi ý id giải đấu kèm logo và cho phép chọn
with st.expander("Gợi ý id giải đấu:"):
    tournament_options = []
    for tournament, logo_url in tournaments.items():
        col1, col2 = st.columns([1, 5])
        with col1:
            st.image(logo_url, width=50)
        with col2:
            st.markdown(tournament)
        tournament_options.append(tournament)
    st.markdown("<h4 style='color: #0072B8;'>Chọn giải đấu:</h4>", unsafe_allow_html=True)  # Tiêu đề nổi bật
    selected_tournament = st.selectbox("🟢 Chọn giải đấu", tournament_options, index=0)  # Thêm biểu tượng

# Hiển thị gợi ý id mùa giải kèm logo và cho phép chọn
with st.expander("Gợi ý id mùa giải:"):
    season_options = []
    for season, logo_url in seasons.items():
        col1, col2 = st.columns([1, 5])
        with col1:
            st.image(logo_url, width=50)
        with col2:
            st.markdown(season)
        season_options.append(season)
    st.markdown("<h4 style='color: #0072B8;'>Chọn mùa giải:</h4>", unsafe_allow_html=True)  # Tiêu đề nổi bật
    selected_season = st.selectbox("🟢 Chọn mùa giải", season_options, index=0)  # Thêm biểu tượng


# Tách ID từ lựa chọn của người dùng
team_id_from_select = selected_team.split(" - ")[-1]
tournament_id_from_select = selected_tournament.split(" - ")[-1]
season_id_from_select = selected_season.split(" - ")[-1]

# Giao diện chọn thông tin đội bóng với ID tự động điền từ lựa chọn
st.markdown("### Nhập ID thủ công hoặc sử dụng từ gợi ý:")

team_id = st.text_input("Nhập team ID:", value=team_id_from_select)
tournament_id = st.text_input("Nhập tournament ID (Giải đấu):", value=tournament_id_from_select)
season_id = st.text_input("Nhập season ID (Mùa giải):", value=season_id_from_select)

# Hiển thị thông tin đã chọn
st.write(f"Bạn đã chọn đội bóng từ gợi ý: {selected_team}")
st.write(f"Giải đấu từ gợi ý: {selected_tournament}")
st.write(f"Mùa giải từ gợi ý: {selected_season}")
st.write("HÃY KIỂM TRA KĨ ĐỘI BÓNG CỦA BẠN CÓ CHƠI Ở GIẢI ĐẤU VÀ MÙA GIẢI BẠN CHỌN KHÔNG!")

# Khi nhấn nút "Lấy Dữ Liệu"
if st.button("Lấy Dữ Liệu"):
    # Ưu tiên giá trị nhập thủ công, nếu không có sẽ dùng từ gợi ý
    final_team_id = team_id if team_id else team_id_from_select
    final_tournament_id = tournament_id if tournament_id else tournament_id_from_select
    final_season_id = season_id if season_id else season_id_from_select

    if final_team_id and final_tournament_id and final_season_id:
        with st.spinner('Đang tải dữ liệu...'):
            data = get_team_data(final_team_id, final_tournament_id, final_season_id)

            # Kiểm tra nếu không có dữ liệu trả về
            if not data or 'topPlayers' not in data:
                st.error("Không có dữ liệu cho đội bóng, giải đấu hoặc mùa giải đã chọn. Vui lòng kiểm tra lại.")
            else:
                player_stats = {}
                keys = ['rating', 'goals', 'assists', 'totalShots', 'shotsOnTarget',
                        'accuratePasses', 'keyPasses', 'accurateLongBalls',
                        'successfulDribbles', 'tackles', 'interceptions']

                for key in keys:
                    for player_info in data.get('topPlayers', {}).get(key, []):
                        player = player_info.get('player', {})
                        statistics = player_info.get('statistics', {})
                        player_name = player.get('name')

                        if player_name not in player_stats:
                            player_stats[player_name] = {
                                'name': player_name,
                                'position': player.get('position'),
                                'type': statistics.get('type'),
                                'appearances': statistics.get('appearances')
                            }

                        player_stats[player_name][key] = statistics.get(key)

                # Tạo tập hợp các khóa duy nhất
                    fieldnames = set()
                    for stats in player_stats.values():
                        fieldnames.update(stats.keys())
                    fieldnames = list(fieldnames)

                # Lưu dữ liệu vào file CSV
                file_name = f"{final_team_id}_{final_tournament_id}_{final_season_id}.csv"
                with open(file_name, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(player_stats.values())

                st.success(f"Dữ liệu đã được crawl và lưu vào file {file_name}")

                # Hiển thị file dữ liệu vừa crawl
                data_df = pd.DataFrame(player_stats.values())
                st.write(data_df.head())

                # Phần thống kê cả mùa
                st.title('📊 Thống Kê Cầu Thủ Mùa Giải 📊')

                # Input for file name
                file_name_input = st.text_input("Tự động phân tích dữ liệu", value=file_name)

                if file_name_input:
                    try:
                        # Load data
                        data = pd.read_csv(file_name_input)

                        # Convert data types
                        data['assists'] = pd.to_numeric(data['assists'], errors='coerce')
                        data['keyPasses'] = pd.to_numeric(data['keyPasses'], errors='coerce')
                        data['goals'] = pd.to_numeric(data['goals'], errors='coerce')
                        data['tackles'] = pd.to_numeric(data['tackles'], errors='coerce')

                        # Tạo báo cáo thống kê
                        report = {
                            'Total Goals': data['goals'].sum(),
                            'Total Assists': data['assists'].sum(),
                            'Total Key Passes': data['keyPasses'].sum(),
                            'Total Tackles': data['tackles'].sum(),
                        }

                        # Tạo biểu đồ cho các chỉ số tổng quát
                        fig, ax1 = plt.subplots(figsize=(10, 6))

                        # Biểu đồ cho Goals và Assists
                        goals_bars = ax1.bar(['Total Goals', 'Total Assists'], 
                                              [report['Total Goals'], report['Total Assists']], 
                                              color=['blue', 'orange'], alpha=0.7)
                        ax1.set_ylabel('Goals & Assists', color='black', fontsize=12)
                        ax1.tick_params(axis='y', labelcolor='black')
                        ax1.set_ylim(0, max(report['Total Goals'], report['Total Assists']) * 1.2)

                        # Thêm giá trị lên trên các cột của Goals và Assists
                        for bar in goals_bars:
                            yval = bar.get_height()
                            ax1.text(bar.get_x() + bar.get_width()/2, yval + 1, 
                                     f'{yval:.0f}', ha='center', va='bottom', fontsize=10, color='black')

                        # Tạo một trục y thứ hai cho Key Passes và Tackles
                        ax2 = ax1.twinx()
                        tackles_bars = ax2.bar(['Total Key Passes', 'Total Tackles'], 
                                                [report['Total Key Passes'], report['Total Tackles']], 
                                                color=['green', 'red'], alpha=0.7, width=0.4, align='edge')
                        ax2.set_ylabel('Key Passes & Tackles', color='black', fontsize=12)
                        ax2.tick_params(axis='y', labelcolor='black')
                        ax2.set_ylim(0, max(report['Total Key Passes'], report['Total Tackles']) * 1.2)

                        # Thêm giá trị lên trên các cột của Key Passes và Tackles
                        for bar in tackles_bars:
                            yval = bar.get_height()
                            ax2.text(bar.get_x() + bar.get_width()/2, yval + 1, 
                                     f'{yval:.0f}', ha='center', va='bottom', fontsize=10, color='black')

                        # Vẽ đường ngăn cách giữa các nhóm cột
                        plt.axvline(x=1.5, color='black', linestyle='--', linewidth=1)

                        # Thiết lập tiêu đề và hiển thị biểu đồ
                        plt.title('Báo Cáo Thống Kê Chỉ Số Của Toàn Đội Trong Mùa Giải', fontsize=16, fontweight='bold', color='navy')
                        plt.grid(axis='y', linestyle='--', alpha=0.7)
                        plt.tight_layout()

                        # Hiển thị biểu đồ
                        st.pyplot(fig)

                        # Get top 3 players for each category
                        top_scorers = data.nlargest(3, 'goals')
                        top_assist_providers = data.nlargest(3, 'assists')
                        top_key_passes = data.nlargest(3, 'keyPasses')
                        top_tacklers = data.nlargest(3, 'tackles')

                        # Function to plot bar charts for top players
                        def plot_top_players(top_players, stat, title, color):
                            fig, ax = plt.subplots()
                            bars = ax.bar(top_players['name'], top_players[stat], color=color, edgecolor='black', linewidth=1.5)
                            ax.set_title(title, fontsize=16, fontweight='bold', color='navy')
                            ax.set_ylabel(stat.capitalize(), fontsize=14)
                            ax.set_ylim(0, top_players[stat].max() * 1.2)
                            ax.grid(axis='y', linestyle='--', alpha=0.7)
                            for bar in bars:
                                yval = bar.get_height()
                                ax.text(bar.get_x() + bar.get_width() / 2, yval + 0.1, f'{yval:.0f}', ha='center', va='bottom', fontsize=12, color='black')
                            st.pyplot(fig)

                        # Top 3 Goals
                        st.header('⚽ Top 3 Cầu Thủ Có Bàn Thắng Cao Nhất ⚽')
                        st.write(top_scorers[['name', 'goals', 'rating']])
                        plot_top_players(top_scorers, 'goals', 'Top 3 Cầu Thủ Có Bàn Thắng Cao Nhất', 'purple')

                        # Top 3 Assists
                        st.header('🎯 Top 3 Cầu Thủ Kiến Tạo Nhiều Nhất 🎯')
                        st.write(top_assist_providers[['name', 'assists', 'rating']])
                        plot_top_players(top_assist_providers, 'assists', 'Top 3 Cầu Thủ Kiến Tạo Nhiều Nhất', 'orange')

                        # Top 3 Key Passes
                        st.header('📊 Top 3 Cầu Thủ Có Đường Chuyền Chính Xác Nhiều Nhất 📊')
                        st.write(top_key_passes[['name', 'keyPasses', 'rating']])
                        plot_top_players(top_key_passes, 'keyPasses', 'Top 3 Cầu Thủ Có Đường Chuyền Chính Xác Nhiều Nhất', 'green')

                        # Top 3 Tackles
                        st.header('🛡️ Top 3 Cầu Thủ Có Số Pha Tắc Bóng Cao Nhất 🛡️')
                        st.write(top_tacklers[['name', 'tackles', 'rating']])
                        plot_top_players(top_tacklers, 'tackles', 'Top 3 Cầu Thủ Có Số Pha Tắc Bóng Cao Nhất', 'red')

                    except Exception as e:
                        st.error(f"Có lỗi xảy ra khi đọc file: {e}")



