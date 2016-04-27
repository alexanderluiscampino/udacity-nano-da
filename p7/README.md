# P7: Data Analyst Interview Dry-Run Review

##  Questions (6 total)

### Question 1 - Describe a data project you worked on recently.

The most recent project that I worked on was data visualization. I had 
to select a dataset and create a graphic to represent it. The dataset
I chose was Titanic passengers. I created the chart to show the
relationship between passenger class, sex and age and the outcome
(survived or died). According to my findings, females in 1st class had
the best chance of survival, and males in 3rd class fared the worst. 

### Question 2 - You are given a ten piece box of chocolate truffles.

You know based on the label that six of the pieces have an orange cream 
filling and four of the pieces have a coconut filling. If you were to eat 
four pieces in a row, what is the probability that the first two pieces 
you eat have an orange cream filling and the last two have a coconut
filling?

 Ate    | Probability | Cream left | Coconut left 
--------|-------------|------------|-------------
 -      |      -      | 6          | 4
 Cream  | 6/10        | 5          | 4
 Cream  | 5/9         | 4          | 4
 Coco   | 1/2         | 4          | 3
 Coco   | 3/7         | 4          | 2
 
Total:

```
0.6 * 5/9 * 0.5 * 3/7 = 0.07
```

### Follow up question:

If you were given an identical box of chocolates and again eat four 
pieces in a row, what is the probability that exactly two contain 
coconut filling?

Let's code Cream as 0 and Coconut as 1. We have 6 possible
combinations allowing us to get 2 of the 1s:

1, 1, 0, 0
0, 1, 1, 0
0, 0, 1, 1
1, 0, 0, 1
1, 0, 1, 0
0, 1, 0, 1

while the number of all possible combinations is `4^2=16`. Therefore,
we can get a 2-coconut outcome with a probability of `6/16=3/8=0.375`.

### Question 3 - Given the table users:

        Table "users"        
| Column      | Type      |
|-------------|-----------|
| id          | integer   |
| username    | character |
| email       | character |
| city        | character |
| state       | character |
| zip         | integer   |
| active      | boolean   |

construct a query to find the top 5 states with the highest number of 
active users. Include the number for each state in the query result.
Example result:

| state      | num_active_users |
|------------|------------------|
| New Mexico | 502              |
| Alabama    | 495              |
| California | 300              |
| Maine      | 201              |
| Texas      | 189              |

```sql
select state, count(id) as num_active_users from users
order by count(id) desc
limit 5
```

### Question 4 - Define a function first_unique

that takes a string as input and returns the first non-repeated (unique)
character in the input string. If there are no unique characters return
None. Note: Your code should be in Python.

```
def first_unique(string):
    # Your code here
    return unique_char

> first_unique('aabbcdd123')
> c

> first_unique('a')
> a

> first_unique('112233')
> None
```

```python
def first_unique(string):
    seen = set([])
    for i in range(len(string)):
        letter = string[i]
        if letter not in seen and letter not in string[i+1:]:
            return letter
        seen.add(letter)
    return None

```

### Question 5 - What are underfitting and overfitting

in the context of Machine Learning? How might you balance them?

Underfitting is the situation when the model does not capture the trend in
data well, i.e. even on training set, performance is not good. Overfitting
is when the model shows good results on training set, but poor results on 
new data. Validation and cross-validation of the model are the usual ways
to fix it.

Before answering the final question, insert a job description for a data analyst position of your choice!

Your answer for Question 6 should be targeted to the company/job-description you chose.

### Question 6 - If you were to start your data analyst position today,

what would be your goals a year from now?

Job description (http://www.parsely.com/jobs/#software_engineer):

```
Software Engineer

We are hiring a software engineer to work on our real-time analytics 
dashboard. Pythonistas and JavaScript hackers especially desired.

Our analytics platform helps digital storytellers at some of the web's 
best sites, such as Arstechnica, New Yorker, Mashable, The Next Web, 
and many more. In total, our analytics backend system needs to 
handle over 50 billion monthly events from over 475 million monthly 
unique visitors.

We are currently looking for software engineers to help us build the 
best real-time analytics dashboard the world has ever seen. The only 
requirement is some experience in Python/JavaScript. Bonus points for 
an interest in information visualization, Edward Tufte, and d3.js. 
To see an example of how we work, check out the blog post, "Whatever It Takes".

Responsibilities

Write code using the best practices.
Analyze data at massive scale.
Brainstorm new product ideas and directions with team and customers.
Master cloud technologies and systems.
Learn, grow, and succeed in your career.

Requirements

Ideally 2-3 years experience in technology, but no minimum experience required.
Self-sufficient, but works well with others.
Highly organized and disciplined about self-improvement.
Open source contributions and publicly scrutable code available.
Some background in Python and/or JavaScript.

```

(I got this job description from my current company jobs page, because
right now I'm happy with my job).

A year from now, I'd like to be a team member who not only knows how to
perform the day-to-day tasks, but also has a view into the future and 
is able to predict both what features the customers will want on the
front-end, and what challenges we may encounter on the back-end (such as
scaling, improving availability and fault tolerance). I want to be able
to "put out fires", make useful suggestions as to what to do next, and
help out younger team members. I want to learn the technical stack and
keep it updated as requirements change. I want the company to never
be unhappy about hiring me.
