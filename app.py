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

# Thiết lập giao diện
st.image('football_banner.jpeg', use_column_width=True)  # Ảnh banner bóng đá
st.title("⚽ Crawl Dữ Liệu Cầu Thủ Bóng Đá ⚽")

st.markdown("""
    **Chào mừng bạn đến với trang thống kê bóng đá!**
    Hãy nhập các thông tin cần thiết và chúng tôi sẽ lấy dữ liệu về đội bóng của bạn.
""")

# Giao diện chọn thông tin đội bóng
team_id = st.text_input("Nhập team ID:")
tournament_id = st.text_input("Nhập tournament ID (Giải đấu):")
season_id = st.text_input("Nhập season ID (Mùa giải):")

# Khi nhấn nút "Crawl Dữ Liệu"
if st.button("Crawl Dữ Liệu"):
    if team_id and tournament_id and season_id:
        with st.spinner('Đang tải dữ liệu...'):
            data = get_team_data(team_id, tournament_id, season_id)

        if data:
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

            # Lưu dữ liệu vào file CSV
            file_name = f"{team_id}_{tournament_id}_{season_id}.csv"
            fieldnames = list(next(iter(player_stats.values())).keys())
            with open(file_name, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(player_stats.values())

            st.success(f"Dữ liệu đã được crawl và lưu vào file {file_name}")

            # Hiển thị file dữ liệu vừa crawl
            data_df = pd.DataFrame(player_stats.values())
            st.write(data_df.head())
        else:
            st.error("No data retrieved.")
    else:
        st.error("Vui lòng nhập đầy đủ thông tin!")

# Phần thống kê cả mùa
st.title('📊 Thống Kê Cầu Thủ Mùa Giải 📊')

# Input for file name
file_name = st.text_input("Nhập tên file CSV (có đuôi):")

if file_name:
    try:
        # Load data
        data = pd.read_csv(file_name)

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

    except FileNotFoundError:
        st.error(f"File {file_name} không tồn tại!")
else:
    st.info("Vui lòng nhập tên file CSV để xem thống kê!")
