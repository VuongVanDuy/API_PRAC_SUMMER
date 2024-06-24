import requests
import json

BASE_URL = 'http://127.0.0.1:5000'
TOKEN = 'token1'  # Thay thế bằng token hợp lệ của bạn

# Headers chung
headers = {
    'Authorization': TOKEN,
    'Content-Type': 'application/json'
}

# Hàm để thêm người dùng mới
def add_user(username, password, link_icon):
    url = f"{BASE_URL}/user"
    data = {
        'username': username,
        'password': password,
        'link_icon': link_icon
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Hàm để lấy tất cả người dùng
def get_users():
    url = f"{BASE_URL}/users"
    response = requests.get(url, headers=headers)
    return response.json()

# Hàm để thêm đánh giá mới
def add_review(id_user, id_route, star_vote, comment):
    url = f"{BASE_URL}/review"
    data = {
        'id_user': id_user,
        'id_route': id_route,
        'star_vote': star_vote,
        'comment': comment
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Hàm để lấy đánh giá của một tuyến đường cụ thể
def get_reviews_of_route(id_route):
    url = f"{BASE_URL}/reviews/{id_route}"
    response = requests.get(url, headers=headers)
    return response.json()

# Hàm để cập nhật link_icon của người dùng
def update_link_icon(username, link_icon):
    url = f"{BASE_URL}/user/{username}/link_icon"
    data = {
        'link_icon': link_icon
    }
    response = requests.put(url, headers=headers, json=data)
    return response.json()

# Hàm để cập nhật mật khẩu của người dùng
def update_password(username, password):
    url = f"{BASE_URL}/user/{username}/password"
    data = {
        'password': password
    }
    response = requests.put(url, headers=headers, json=data)
    return response.json()

# Ví dụ sử dụng các hàm trên
if __name__ == "__main__":
    # # Thêm người dùng mới
    # user_response = add_user('user1', 'password1', './pictures/avatar_default.png')
    # print(f"Add User Response: {user_response}")

    # Lấy tất cả người dùng
    users_response = get_users()
    print(f"Get Users Response: {json.dumps(users_response, indent=2)}")

    # # Thêm đánh giá mới
    # review_response = add_review(1, 1062, 5, 'Great route!')
    # print(f"Add Review Response: {review_response}")

    # # Lấy đánh giá của một tuyến đường
    # reviews_response = get_reviews_of_route(1062)
    # print(f"Get Reviews of Route Response: {json.dumps(reviews_response, indent=2)}")

    # # Cập nhật link_icon của người dùng
    # update_icon_response = update_link_icon('user1', './pictures/new_avatar.png')
    # print(f"Update Link Icon Response: {update_icon_response}")

    # # Cập nhật mật khẩu của người dùng
    # update_password_response = update_password('user1', 'new_password1')
    # print(f"Update Password Response: {update_password_response}")
