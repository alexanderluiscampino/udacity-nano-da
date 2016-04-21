# Summary

This visualization shows survival on Titanic, depending on three factors:
 
* Passenger class
* Sex
* Age

On X axis, we have passenger class, and male vs female within each
class.

On Y axis, we have the age group.

Survivors are plotted in red, and the ones who didn't make it in blue.

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

![Original chart](titanic-1.png "Survival on Titanic")

# Feedback

TODO

#  Resources

* http://dimplejs.org/examples_index.html
* https://github.com/mbostock/d3/wiki
* http://stackoverflow.com/questions/25774821/dimple-js-axis-labels
* http://www.d3noob.org/2014/02/grouping-and-summing-data-using-d3nest.html