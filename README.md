<div id="header" align="center">
  <img src="https://media.giphy.com/media/M9gbBd9nbDrOTu1Mqx/giphy.gif" width="100"/>
</div>
<h1 align="center">Hi 👋, I'm Adrian</h1>
<h3 align="center">A passionate automation tester and python developer from Romania</h3>

<p align="left"> <img src="https://komarev.com/ghpvc/?username=adrianmacovei&label=Profile%20views&color=0e75b6&style=flat" alt="adrianmacovei" /> </p>

- 🔭 I’m currently working on **API Testing**

- 🌱 I’m currently learning **Selenium, Behave, Postman, Manual Testing**

- 📫 How to reach me **adrianmacovei17@gmail.com**

- 📄 Know about my experiences [https://adrianmacovei17.wixsite.com/1996](https://adrianmacovei17.wixsite.com/1996)

#

<h3 align="left">Connect with me:</h3>
<p align="left">
<a href="https://linkedin.com/in/adrian-macovei-4b3a23169" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/linked-in-alt.svg" alt="adrian-macovei-4b3a23169" height="30" width="40" /></a>
<a href="https://instagram.com/adrian_m105" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/instagram.svg" alt="adrian_m105" height="30" width="40" /></a>
</p>

#

<h3 align="left">Languages and Tools:</h3>
<p align="left"> <a href="https://www.python.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a> <a href="https://www.selenium.dev" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/detain/svg-logos/780f25886640cef088af994181646db2f6b1a3f8/svg/selenium-logo.svg" alt="selenium" width="40" height="40"/> </a> <a href="https://pypi.org/project/behave/" target="_blank" rel="noreferrer"> <img src="https://avatars.githubusercontent.com/u/3344102?v=4&s=160" alt="behave" width="40" height="40"/> </a> <a href="https://postman.com" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/getpostman/getpostman-icon.svg" alt="postman" width="40" height="40"/> </a> <a href="https://git-scm.com/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/git-scm/git-scm-icon.svg" alt="git" width="40" height="40"/> </a> <a href="https://www.w3.org/html/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/html5/html5-original-wordmark.svg" alt="html5" width="40" height="40"/> </a> <a href="https://www.mysql.com/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/mysql/mysql-original-wordmark.svg" alt="mysql" width="40" height="40"/> <a href="https://www.java.com" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/java/java-original.svg" alt="java" width="40" height="40"/> </a> <a href="https://www.atlassian.com/software/jira" target="_blank" rel="noreferrer"> <img src="https://logos-world.net/wp-content/uploads/2021/02/Jira-Emblem-700x394.png" alt="jira" width="40" height="40"/> </a></p>


# API Testing Project

In the current project I test the Simple Book API using two different approach:
-	Testing API with Postman (dedicated GUI application for API testing purpose) and JavaScript for writing tests.
-	Testing API with Python and it’s library Requests (dedicated Python library for API testing)


## Simple Book API testing with  Postman

### Prerequisites
To run the collection need to:
- install first the Postman application from https://www.postman.com/downloads/
- install git from https://gitforwindows.org

### Run the test in the Postman collection with steps billow:
- Create a folder for this project

- Clone the repo on your divice using in terminal command `git clone https://github.com/AdrianMacovei/API-Testing-Project`

- Open Postman

- Follow steps in video:
[![Postman video](https://github.com/AdrianMacovei/data-and-images-for-my-repos/blob/main/-182-Run-Postman-Collection-YouTube.png)](https://youtu.be/k31uzXQ7Dhw)

## Simple Book API testing with Python/Requests

### Prerequisites
To run the Python code need to:
- install python on you laptop/pc https://www.python.org/downloads/
- install Pycharm https://www.jetbrains.com/pycharm/download/#section=windows Community or other IDE (ex Visual Studio Code)
- install git (link above)

### Run test in IDE with steps bellow:
- Create a folder for the project and clone the repo (see in video above)
- Follow the steps in the video to run the test:
[![Pycharm video](https://github.com/AdrianMacovei/data-and-images-for-my-repos/blob/main/pycharm_video.png)](https://youtu.be/k31uzXQ7Dhw)

- If want to create html report run next command in the terminal `pytest --html=report.html --self-contained-html`

### Project structure
 API testing with Python and requests has two main parts:
-	TestCase folder where is the api_test.py file that is the host file for all the test in the project.
-	UserDataAndApiMethods folder has two .txt files that are connected to the api_methods_config and help to save the data on disk (persistence), data like authentication toke and current user data (name and email).


### Tests results

In this project, I create a number of 36 tests that test different functionality of the API. Form the total number 6 failed and 30 passed.
Based on the test result I can make the following recommendations for developers of the API to increase the quality of the product:

- When sending a get request to the endpoint /books with limit 0 and string value in it the API accepts the values and return all books available. There 
  in my opinion, will be better a 4xx response with the return message error "Invalid limit value".

- I tried to change an order attribute id and quantity using a patch request to the endpoint /orders/order_id and the response status code was 204 No content
  the same status code was used to delete the order request and change the customer name of the order. In my opinion, the code should be different because the last two   mentioned (delete and change customer name) make a change in the database but the first two (change quantity and id) don't (value remain the same after I tried to     change it). 
  A recommendation is for all the attributes of order that can't be modified to return a 4xx code with some error message. Even for the delete and customer name update 
  will be great to return some content that informs the person who uses the API that his request makes the change in the data (ex: {"status":"order deleted"} or
  {"status":"customer name updated"}).

  
- Now the order quantity attribute can't be changed but will be a good update for the API if in the future will offer this possibility after that an order can contain   for example more than one book of the same type.
  
- Tried to test if ordering more than the available number of a book will activate some error message and I find that the server doesn’t update the book quantity accordingly with the number of orders for the book. This can be disastrous for a business for example because will go to a situation when the client’s order can’t be honoured just because the stock is not updated properly. The recommendation is to make the server update the book quantity accordingly with the number of orders and to change the value of the attribute available to False when the stock reaches the value of zero.
  
- Finally, I find that in the authentication part the API accepts integer data type in the customer name, can be a good practice if will be changed to accept only string data type.
  
![alt text](https://github.com/AdrianMacovei/data-and-images-for-my-repos/blob/main/report-html%20(5).png)


