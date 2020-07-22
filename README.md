# Scraping project: basketball_reference.com
## We're about to achieve the Moneyball movie, but for Basketball

<p>We scrap data about basketball <strong>players</strong>, <strong>team constitution over the years and by team </strong>
 <strong> and drafts by year</strong>.
<p>In the long run, this project could make it possible to apply data scienceto predict the value of a player
based on his performances and assess how likely he is to become one of the most valuable players.</p>

### Usage
<p>To scrap data about players:</p>
<nano> <strong>python players_scrap.py --start [arg start_letter] --end [arg end_letter]</strong></nano>
<p>This code makes it possible to scrap data about players whose last name is between start_letter ('a' by default)
and end_letter ('z' by default)</p>
<p></p>
<p>To scrap data about drafts:</p>
<nano> <strong>python players_draft.py --start [arg start_year] --end [arg end_year]</strong></nano>
<p>This code makes it possible to scrap data all drafts between start_year (2010 by default)
and end_year (2020 by default)</p>
<p>To scrap data about teams:</p>
<nano> <strong>python teams_draft.py --start [arg start_year] --end [arg end_year] --teams [team1] [team2] [team3] </strong></nano>
<p>This code makes it possible to scrap data all drafts between start_year (by default 2010)
and end_year (by default 2020), for specific teams</p>

### Installation
<p>Run following command:</p>
<nano>pip install -r requirements.txt</nano>

### Tables
<p align="center"><img src="image_tables.pdf"></p>

### Authors & acknowledgement
<p>Thanks to you guys for taking the time to correct us and give us feedback</p>
