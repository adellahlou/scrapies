//npm modules
var fs = require('fs');
var mongoose = require('mongoose');
var connection = mongoose.connect('mongodb://root:Eight123@ds053784.mongolab.com:53784/sccs_scrapeproject');


var rawData = {
	cs1314 : require('./computerScience1314.json').data,
	cs1415 : require('./computerScience1314.json').data,
	cs1516 : require('./computerScience1314.json').data
};

var dataKeys = Object.keys(rawData);
var data = {}

dataKeys.forEach(function(key){
	data[key] = [];
	extractYear(rawData[key], data[key]);
});



var Schema = mongoose.Schema;
var ProcessedSchema = new Schema({
	dataType: String, 
	content : String, 
	time: Date, 
	contentid: String, 
	userid: String
});

var ProcessedModel =  mongoose.model('Scrapie', ProcessedSchema);

dataKeys.forEach(function(key){
	data[key].forEach(function(tuple){
		dbSave(tuple, ProcessedModel);
	});

	console.log("Finished issuing requests");
});




function extractYear(year_raw,year_data){
	year_raw.forEach(function(post){
		extractPost(post, function(data){
			year_data.push(data);
		});
	});
}

function extractPost(post, save){
	var dataType = 'post', 
		content = post.message, 
		time = post.created_time, 
		contentid = post.id,
		userid = post.from.id;

	var dtuple = dataTuple(dataType, content, time, contentid, userid);
	save(dtuple);

	var comments = post.comments;

	if(comments){
		comments = comments.data;
		comments.forEach(function(comment){
			extractComment(comment, save);
		});
	}
}

function extractComment(comment, save){
	var dataType = 'comment', 
		content = comment.message, 
		time = comment.created_time, 
		contentid = comment.id,
		userid = comment.from.id;

	save(dataTuple(dataType, content, time, contentid, userid));
}


function dataTuple(dataType, content, time, contentid, userid){
	return {
		dataType: dataType, 
		content : content, 
		time: time, 
		contentid: contentid, 
		userid: userid
	};
}

function dbSave(tuple, Model){
	var inst = new Model(tuple);

	inst.save(function(err){
		if(err)
			console.log(err);
	});
}


