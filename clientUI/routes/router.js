module.exports = (router) => {
	router.get('/', (req, res) => {

		var inventory = require('../../records/db.json').entries;

		console.log(inventory);
		inventory = inventory.map( (item) => { 
			console.log(inventory);
			return Object.assign({}, item, { gifUrl: '/records/' + item.gifUrl });
			// return item;
		});
		console.log(inventory);
		

		res.render('pages/index', {
			entries: inventory,
		});
	});

	router.get('/about', (req, res) => {
		res.render('pages/about');
	});
}
