module.exports = (router) => {
	router.get('/', (req, res) => {

		var inventory = require('../../records/db.json').entries;

		inventory = inventory.map( (item) => Object.assign(
			{}, 
			item, 
			{ gifUrl: '/records/' + item.gifUrl }
		));

		res.render('pages/index', {
			entries: inventory,
			error: false,
		});
	});

	router.get('/:name', (req, res) => {
		var filePath = __dirname + '/../../records/' + req.params.name + '.json';

		try {
			var item = require(filePath);
			item = Object.assign(
				{}, 
				item, 
				{ gifUrl: '/records/' + item.gifUrl }
			);
			console.log('item', item);
			res.render('pages/index', {
				entries: [item],
				error: false,
			});
		} 
		catch(err) {
			res.render('pages/index', {
				error: true,
			});
		}
	});

	router.get('/about', (req, res) => {
		res.render('pages/about');
	});
}



