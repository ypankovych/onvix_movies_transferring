import requests
from time import sleep
from selenium import webdriver

sign = 'https://onvix.tv/'
sign_in  = 'https://onvix.tv/users/sign_in'
get_favorite = 'https://onvix.tv/playlists/favorites.json?page=1'
goto_movie_link = 'https://onvix.tv/serial/{}'
favorite_button_xpath = '//*[@id="modal_movies_scroll"]/div[2]/div/div[1]/div[1]/div[2]/a[1]'
input_email_xpath = '//*[@id="login_form"]/div[3]/label/input'
input_password_xpath = '//*[@id="login_form"]/div[4]/label/input'
log_in_button_xpath = '//*[@id="login_form"]/button/strong'

def get_favorite_movies(email, password, flag='true'):
    UserSession = requests.Session()
    with UserSession as user_session:
        user_session.post(sign_in, data={
            'user[email]': email,
            'user[password]': password,
            'user[remember_me]': flag
        })
        result = user_session.get(get_favorite).json()
        return [i['token'] for i in result['materials']]

def run_browser(tokens, email, password):
    driver = webdriver.Chrome('ChromeDriver.exe')
    driver.get(sign)
    driver.find_element_by_xpath(input_email_xpath).send_keys(email)
    driver.find_element_by_xpath(input_password_xpath).send_keys(password)
    driver.find_element_by_xpath(log_in_button_xpath).click()
    for token in tokens:
        sleep(1)
        driver.get(goto_movie_link.format(token))
        sleep(2)
        driver.find_element_by_xpath(favorite_button_xpath).click()
    driver.quit()

def main():
    print('Enter data from your old account.')
    old_email = input('email: ')
    old_password = input('password: ')
    print('Collecting old movies...')
    favorites = get_favorite_movies(old_email, old_password)
    print(f'Collected {len(favorites)} movies.')
    print('Enter information from a new account.')
    email = input('email: ')
    password = input('password: ')
    run_browser(favorites, email, password)
    print('Successfully')

if __name__ == '__main__':
    main()