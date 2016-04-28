# P7: Data Analyst Interview Dry-Run Review

##  Questions (6 total)

### Question 1 - Describe a data project you worked on recently.

The most recent project that I worked on was data visualization. I had 
to select a dataset and create a graphic to represent it. The dataset
I chose was Titanic passengers. I created the chart to show the
relationship between passenger class, sex and age and the outcome
(survived or died). According to my findings, females in 1st class had
the best chance of survival, and males in 3rd class fared the worst.

To create the chart, I used dimple.js, but it ended up being not enough 
to create some of the features that I wanted, such as custom legend
formatting and additional axis labels. I used d3 for that.
 
I selected pie chart to represent died/survived people in each
class/sex/age group. Despite its bad reputation (see 
http://www.perceptualedge.com/articles/08-21-07.pdf for example) I think
that in case of only 2 categories to represent, pie charts are acceptable,
and they look more attractive visually than stacked bars. I also chose
to use hues of red for females survived/died, and hues of blue for 
males survived/died, and this was a controversial choice. I had 2 people
that said it "made the graphic more clear because genders really stood
out" and two that said "so many colors made it hard to figure out". I
kept going back and forth on that, but since the tastes differed 50/50,
I went with one that looked more appealing to me.

This was also an interesting project, because this data represents a real
catastrophe, something that affected many people's lives, and it was
so big that it's still being talked of.

### Question 2 - You are given a ten piece box of chocolate truffles.

You know based on the label that six of the pieces have an orange cream 
filling and four of the pieces have a coconut filling. If you were to eat 
four pieces in a row, what is the probability that the first two pieces 
you eat have an orange cream filling and the last two have a coconut
filling?

 Ate    | Probability | O left | C left 
--------|-------------|------------|-------------
 -      |      -      | 6          | 4
 O      | 6/10        | 5          | 4
 O      | 5/9         | 4          | 4
 C      | 1/2         | 4          | 3
 C      | 3/7         | 4          | 2
 
Total:

```
0.6 * 5/9 * 0.5 * 3/7 = 0.07
```

### Follow up question:

If you were given an identical box of chocolates and again eat four 
pieces in a row, what is the probability that exactly two contain 
coconut filling?

We have 6 possible combinations allowing us to get 2 coconat truffles:

C C O O
O C C O
O O C C
C O O C
C O C O
O C O C

So we can calculate the probability of all of them and add them up. 
I wrote a piece of code to do that:

```python
import operator


def take_one(box, truffle):
    """
    Calculate probability of pulling truffle of given type.
    :param box: dict of {type: count}.
    :return (float, box): probability and updated box.
    """
    total_truffles = sum(box.values())
    prob = (0. + box[truffle]) / total_truffles
    if box[truffle]:
        box[truffle] -= 1
    return prob, box


def take_sequence(box, seq):
    """Calculate probability of sequence of truffles.
    :param box: dict of {type: count}.
    :param seq: string
    :return float
    """
    probs = []
    for truffle in seq:
        p, box = take_one(box, truffle)
        probs.append(p)
    return reduce(operator.mul, probs, 1)


if __name__ == '__main__':
    total_prob = 0
    for seq in ['CCOO', 'OCCO', 'OOCC', 'COOC', 'COCO', 'OCOC']:
        box = {'O': 6, 'C': 4}
        ps = take_sequence(box, seq)
        print '- {}: {}'.format(seq, ps)
        total_prob += ps
    print 'Result', total_prob
```

Here is the output:

```
- CCOO: 0.0714285714286
- OCCO: 0.0714285714286
- OOCC: 0.0714285714286
- COOC: 0.0714285714286
- COCO: 0.0714285714286
- OCOC: 0.0714285714286
Result 0.428571428571
```

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
group by state
order by num_active_users desc
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

This solution is short to code and easy to understand. However,
complexity is O(N^2), since we are doing the look-ahead through the 
string for every letter, slightly mitigating it by the `seen` check.
It may be more efficient to:

* create a dict of `letter: (count, index)`: O(N)
* loop through the dict and find key with count=1 and minimal index: O(N)

Here, complexity would be O(2*N).

### Question 5 - What are underfitting and overfitting

in the context of Machine Learning? How might you balance them?

Underfitting is the situation when the model does not capture the trend in
data well, i.e. even on training set, performance is not good. Overfitting
is when the model shows good results on training set, but poor results on 
new data. Validation and cross-validation of the model are the usual ways
to fix it.

Possible causes of underfitting:

* model is too simple
* not enough features
* bad choice of parameters

Possible causes of overfitting:

* too few data points
* too many features
* data has noise

Before answering the final question, insert a job description for a 
data analyst position of your choice!

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

A year from now, I'd like to:

1. Be able to efficiently use Apache Spark and Apache Storm in my work.

How I might achieve that:

* Learn from existing code.
* Use technical documentation.
* Ask questions from more experienced team members.

Those two systems are the foundation of our current data processing
pipeline. We make it work, but problems still come up, and currently
we spend about 20% of development time (1 day every week) on fixing
customer issues that could be prevented if we increased stability and
reliability of the system. I would call it a win if we could cut this
time in half and only need to have a "bug day" once every two weeks.

2. Become an expert in monitoring tools and create a single dashboard
that we can use to diagnose problems arising during the daily data
processing tasks. Use it to determine the bottlenecks and parts of the
pipeline that have problems most often, and potentially would prevent
us from scaling the system to support more events.
