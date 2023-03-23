## Site on Django 4.1.5. Data collection service.
* A service that collects data about vacancies from job search sites and sends them to subscribers. 
* ubscribers of the service are registered by choosing a city and programming language. 
* Once a day, all subscribers who want to receive emails with vacancies are selected and based on their preferences,
a list of URLs is formed, by which parsers are launched to collect vacancies by these parameters. 
* After the parsers have worked, sending letters to those who want to receive the newsletter starts.
