**NOTE: I am not responsible for any people that misuses my script**

# AutoAimsCIT
A simple python bot for **CIT-U (Cebu Institute of Technology University)** to automate tasks in **AIMS**.

## Dependencies

1. Selenium https://pypi.org/project/selenium/
2. selenium-stealth https://pypi.org/project/selenium-stealth/
3. Google Chrome https://www.google.com/intl/en_ph/chrome/


## Usage

To automatically submit tasks use this code below

**For Automatic Faculty Evaluation**


```
from AutoAimsCIT import Semester, Rating
from AutoAimsCIT import AutoAIMS


if "__main__" == __name__:
    autoaims = AutoAIMS()

    autoaims.login("[your AIMS username]", "your AIMS password")
    autoaims.automate_faculty_evaluation(
        school_year="2324",
        semester=Semester.SECOND,
        rating=Rating.GOOD,
        meet_again=True
    )

    autoaims.driver.close()
```

if you want to show the window change the AutoAIMS constructor to true:

```
autoaims = AutoAIMS(True)
```










