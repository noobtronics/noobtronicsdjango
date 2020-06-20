const penthouse = require('penthouse')
const fs = require('fs')

penthouse({
  url: 'https://localhost',
  css: '/Users/Nikhil/Desktop/legacy/noobtronicsdjango/mysite/static/css/bulma/mystyle.min.css',
  width: 1366,
  height: 768,
  renderWaitTime: 5000,
  keepLargerMediaQueries: true,
  blockJSRequests: false,
  screenshots: {
    basePath: 'homepage', // absolute or relative; excluding file extension
    type: 'jpeg', // jpeg or png, png default
    quality: 80 // only applies for jpeg type
  }
})
.then(criticalCss => {
  // use the critical css
  fs.writeFileSync('homepage.min.css', criticalCss);
})
