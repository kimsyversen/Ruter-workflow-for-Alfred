# Ruter workflow for Alfred
![Workflow demo](http://i.imgur.com/dSriim7.gif)

This workflow allows you to manage your public transport routes in Oslo and Akershus (Norway) through Alfred.

## Usage

1. Go to [Ruter's website](https://ruter.no/) and search for a route. Don't select points indicated by ![Position](http://i.imgur.com/IUsgVfW.png) ![House](http://i.imgur.com/6N7A0i1.png))
2. Copy the URL (e.g. https://ruter.no/reiseplanlegger/Mellom/Fra/(3012165)Grefsen%20stadion%20(Oslo)/til/(3010013)Jernbanetorget%20(foran%20Oslo%20S)%20(Oslo)/etter/#st:0,sp:0,bp:0)
3. Open Alfred and type "ruter" and select create route
4. Give the route a name and paste the URL

## Feedback / Issues / Improvements
This workflow may contain bugs and is released "as is". If you encounter a bug or want to suggest improvements, please let me know [here](https://github.com/kimsyversen/ruter_workflow_alfred/issues). You are also very welcome to contribute.

## Disclaimer
This workflow is developed on a private basis and have no relation to Ruter other than it uses the official [Ruter API](https://ruter.no/labs/). 

## FYI
* *This workflow is probably only of interest of those living in Oslo and Oslo and Akershus (Norway). It might serve as a basis for developing similar workflows in other cities/countries.*
* *Routes with a start/stop points indicated the following icons is not supported* ![Position](http://i.imgur.com/IUsgVfW.png) ![House](http://i.imgur.com/6N7A0i1.png)
* All searches are based on the current time. It is currently no way to plan trips hours ahead.

## Thanks to
[Dean Jackson](https://github.com/deanishe/) for the workflow [library](https://github.com/deanishe/alfred-workflow) and [icons](http://icons.deanishe.net/)

## License
MIT License

Copyright (c) 2017 Kim Syversen

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
