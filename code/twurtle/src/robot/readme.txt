This will be python code for the raspberry pi as follows:

- a module to drive stepper motors, 2 instances of a motor on GPIO's
  driven by a motor drive chip (4 inputs per motor)
  
- GPIOs to sense collision sensors on all 4 corners

- a turtle API with the same level1 commands as the javascript API
  including estimated position and direction, and collision detection
  estimation and collision detection from switches to clamp movements
  
- a solenoid driver to move the pen up and down

- some maths to calculate based on the wheel base and diameter, how to
  move forward a specific step distance, and how to rotate around the pen
  axis a specific number of degrees
  
- url fetcher that fetches from a nominated ip address (php page) to poll
  for new commands, probably from a web server either on localhost or
  on the web.

- a main loop that polls for commands and actions commands

- an inactivity timeout in main loop that lifts the pen after a few seconds
  to prevent blotching and replaces it before moving again
  
- a pc simulation written in pygame with the same API
  and including IO simulation at the GPIO level.
  
- a distance measurer in the top loop. On a timer, every 5 minutes, it
  posts to a php page the values of counters such as number of degrees
  rotated in total and distance travelled total. This php page then
  makes a connection as a proxy to twitter and tweets the present
  counter values
  
- the command receipt and value tweeting will be abstracted via a library
  call - this links to php pages, but could just as well connect via twitter
  over a direct internet connection and receive commands in a queue from
  twitter and send tweets every 5 minutes to a real twitter account or
  hash tag.
  
  
  
END.

