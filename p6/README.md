# Summary

Here is the the [interactive version](http://bl.ocks.org/j-bennet/raw/219cf6b3cebc5b93a310308c64231cc6/).

This visualization shows survival on Titanic, depending on three factors:
 
* Passenger class
* Sex
* Age

On X axis, we have passenger class, and male vs female within each
class.

On Y axis, we have the age group.

Survivors are plotted in lighter color, and the ones who didn't make it
in darker color. Blue for males, red for females.

# Design

The data was transformed to first place each passenger into one of the
age groups as follows:

1. 0 - 18 years old (children)
2. 19 - 49 years old (adults)
3. 50 and up (older people)
4. Unknown.

Then, passengers were grouped by:

* Class
* Sex
* Age group
* Survival.

Initially, I tried bubble chart, and used number of people in each group
to size the bubbles. However, most of the passengers fall into the group
from 19-49 years old in 3rd class. Then that one bubble becomes very
large, and the rest of them are very small in comparison, and it's not
easy to see ratio of survival in each group.

After that, I chose pie chart to display the groups, and gave them all a
fixed size. This way, it's easier to see which groups were the luckiest.

## Version 1

![Original chart](titanic-1.png "Survival on Titanic, v1")

# Feedback on version 1

* Red associated with "good" and blue with "bad" is counter-intuitive.
* It took a while to spot that there are two columns of pies in
  each passenger class to represent males and females.

## Version 2

![Version 2](titanic-2.png "Survival on Titanic, v2")

# Feedback on version 2

* Because you can't see absolute numbers on chart (unless you hover over),
  it's hard to tell which groups are more representative of a tendency,
  and which are not. For example, all females of age 50+ in third class
  survived, which seems to go against the tendency. But then, this group
  only contains one person, so it is not really representative.

![Version 3](titanic-3.png "Survival on Titanic, v3")

#  Resources

* http://dimplejs.org/examples_index.html
* https://github.com/mbostock/d3/wiki
* http://stackoverflow.com/questions/25774821/dimple-js-axis-labels
* http://www.d3noob.org/2014/02/grouping-and-summing-data-using-d3nest.html
* http://stackoverflow.com/questions/28306308/how-to-draw-labels-on-dimple-js-donut-or-pie-chart
