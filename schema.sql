/*=====[ Step 1: delete all existant tables ]=====*/
drop table if exists comments;
drop table if exists images;


/* Table: comments
 *---------------
 * will contain all comments w/ their associated images ids
 */
create table comments (
	id integer primary key autoincrement,
	text text not null,
	image_id text not null
);


/* Table: images
 * -------------
 * will contain information on each of the images, including 
 * id, url, artist, description
 */
create table images (
	id integer primary key autoincrement,
	url text not null,
	artist text not null,
	description text not null
)
