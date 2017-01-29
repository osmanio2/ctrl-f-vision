var rp = require('request-promise');

var URL = 'http://localhost:3000';

module.exports = (router) => {
	router.get('/', (req, res) => {

		rp(URL + '/files/db.json')
			.then((json) => {
				console.log(json);
				var inventory = JSON.parse(json).entries.map( (item) => Object.assign(
					{}, 
					item, 
					{ gifUrl: URL + '/files/' + item.gifUrl }
				));
				res.render('pages/index', {
					entries: inventory,
					error: false,
				});
			})
			.catch((err) => {
				console.log(err);
				res.render('pages/index', {
					error: true,
				});
			});
	});

	router.get('/:name', (req, res) => {

		rp(URL + '/files/' + req.params.name +'.json')
			.then((json) => {
				console.log(json);
				var item = JSON.parse(json);
				item = Object.assign(
					{}, 
					item, 
					{ gifUrl: URL + '/files/' + item.gifUrl }
				);
				console.log('item', item);
				res.render('pages/index', {
					entries: [item],
					error: false,
				});
			})
			.catch((err) => {
				console.log(err);
				res.render('pages/index', {
					error: true,
				});
			});
	});

	router.get('/files/:file', (req, res) => {
		var fileName = req.params.file;
		res.sendFile(fileName, {root: __dirname + '/../../records'}, (err) => {
			if (err) {
				console.log(err);
				res.status(err.status).end();
			}
			else {
				console.log('Sent:', fileName);
			}
	  });
	});

	router.get('/about', (req, res) => {
		res.render('pages/about');
	});
}



