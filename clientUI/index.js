var path = require('path');
var morgan = require('morgan');
var express = require('express');
var bodyParser = require('body-parser');

var app = express();
var router = express.Router();

/*	Load views
*/
// views is directory for all template files
app.set('views', __dirname + '/views');
app.set('view engine', 'ejs');

/*  Use morgan for HTTP request logging in dev and prod
*/
app.use(morgan('combined'));

/*  Serve static assets
*/
app.use('/', express.static(path.join(__dirname, 'public')));
app.use('/records', express.static(path.join(__dirname, '/../records')));

/*  Parse incoming form-encoded HTTP bodies
*/
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.set('json spaces', 2);

// Configure application routes
var routes = require('./routes/router');
routes(router);
app.use(router);

app.get('/', (req, res) => {
	res.send('Root');
	// res.render('pages/index');
});

app.get('*', (req, res) => {
  res.status(404).send('Not found');
});

/*   Start the server
*/
app.set('port', (process.env.PORT || 3000));
app.listen(app.get('port'), () => {
	console.log('Node app is running on port', app.get('port'));
});

module.exports = app;


