# data for registration user
expected_keys_successful_registration_user = ['success', 'user', 'accessToken', 'refreshToken']
key_registration_user = ['email', 'name']
text_registration_same_user = {'success': False, 'message': 'User already exists'}
text_registration_user_two_param = {'success': False, 'message': 'Email, password and name are required fields'}
parameters_list = [['email', 'password'], ['password', 'name'], ['email', 'name']]

# data for login user
expected_keys_successful_login_user = ['success', 'user', 'accessToken', 'refreshToken']
key_login_user = ['email', 'name']
text_login_user_unauthorized = {'success': False, 'message': 'email or password are incorrect'}
login_data_unauthorized = [['email_true', 'password_false'], ['email_false', 'password_true'],
                           ['email_true', 'password_none'], ['email_none', 'password_true']]

# data for change data user
expected_keys_successful_change_data_user = ['success', 'user']
key_change_user = ['email', 'name']
list_new_data_user = [['email_new', 'name'], ['email', 'name_new'], ['email_new', 'name_none'],
                      ['email_none', 'name_new']]
text_change_data_user_unauthorized = {'success': False, 'message': 'You should be authorised'}
text_change_data_user_forbidden = {'success': False, 'message': 'User with such email already exists'}

# data for create order
expected_keys_successful_create_order = ['success', 'name', 'order']
key_create_order = ['number']
text_create_order_bad_request = {'success': False, 'message': 'Ingredient ids must be provided'}
text_create_order_unauthorized = {'success': False, 'message': 'You should be authorised'}
list_without_ingredients = []
list_uncorrect_hash_ingredients = ['aaaaa', '010101']

# data get users orders
list_count_burgers = [1, 49, 50, 51, 52]
expected_keys_successful_get_users_orders = ['success', 'orders', 'total', 'totalToday']
keys_get_orders = ['ingredients', '_id', 'status', 'number', 'createdAt', 'updatedAt']
list_status_orders = ['done', 'cancel']
text_get_order_whithout_orders = {'orders': [], 'success': True, 'total': 0, 'totalToday': 0}
text_get_order_unauthorized = {'success': False, 'message': 'You should be authorised'}

