# jack_bunny
Inspired by Facebook's [bunnylol](https://github.com/ccheever/bunny1) search engine. The version that's currently open on github is 
pretty old and had some old dependencies so I thought it'd be easier to just write a more modern one. This one is still pretty basic and
most likely has security holes that I'll run into later. Just wanted to get something off the ground and I'll add in more features time
permitting.

Visit [link](http://ec2-54-214-90-54.us-west-2.compute.amazonaws.com) to setup using this version that I'm hosting.

### Commands
List of currently supported commands

* `g [insert query]` searching google
* `p [insert class number]` make a piazza search, kinda personalized just for jack lol
* `fb [insert query]` searching on facebook. defaults on fb homepage
* `cpp [insert query]` searches for syntactical cpp terms on cppreference.com
* `w [insert query]` searches wikipedia, defaults on english wikipedia page
* `yt [insert query]` make a youtube search. If not query is passed in, defaults to the youtube homepage
* `gm [insert number from 0-n where n = number of gmail accounts - 1]` opens up gmail. If no argument specificed, opens up the first account. Can open up alternative accounts with arguments
* `help` returns a list of usable commands

### How to write your own commands
I think extending this is pretty intuitive for now. Just add in new methods to the Commands class. It might be a little confusing cause
everything is happening in the `jack_bunny.py` file, I'll probably modularize this later when I have the time.

### How to host your own server
I hosted this on an Amazon EC2 server, configured with nginx and gunicorn so I'll walk through the steps I went through.

The first step is to clone this repo on the server you want to run this on and download all the dependencies. These should all
be in the `requirements.txt` file so something like `pip3 install -r /path/to/requirements.txt` should work. If you run into any
issues, the only python libraries this really uses are [`flask`](http://flask.pocoo.org/docs/0.12/installation/) and 
[`wikipedia`](https://pypi.python.org/pypi/wikipedia) so downloading those should resolve any problems.

There are additional packages you need to host this. The first is `nginx`. To install this, you can simply use 
`sudo apt-get install nginx`. We will also need to install `gunicorn` and to do this you can use `pip3 install gunicorn`.

The idea behind this is that we will use `gunicorn` to run this on the localhost on some unused port. We will then use
`nginx` as a reverse proxy so that it will hand off the request it received to `gunicorn` and then `gunicorn` will serve
that to `nginx` which will the be given to the user. 

So how do we do this?

First we want to get `gunicorn` running. The command to run is `gunicorn jack_bunny:app -p jack_bunny.pid -D`. 
In this command, `jack_bunny` represents the file name without the `.py` and `app` represents the Flask app. We add the `-D` tag so that
this will be running in the background, even when we close out. the `-p jack_bunny.pid` saves the process_id to this file so if you want
to kill this process you can just kill -9 it. 

Now we just have to setup `nginx` because this is still only running locally. 

I first created this new config file at `/etc/nginx/sites-available/jack_bunny`
```
# /etc/nginx/sites-available/jack_bunny

# Redirect www.[insert server name].com to [insert server name].com
server {
        server_name www.[insert server name].com;
        rewrite ^ http://[insert server name].com/ permanent;
}

# Handle requests to exploreflask.com on port 80
server {
        listen 80;
        server_name [insert server name].com;

                # Handle all locations
        location / {
                        # Pass the request to Gunicorn
                proxy_pass http://127.0.0.1:8000;

                # Set some HTTP headers so that our app knows where the
                # request really came from
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
}
```
Then I created symlink here.
```
$ sudo ln -s \
/etc/nginx/sites-available/jack_bunny \
/etc/nginx/sites-enabled/jack_bunny
```
After restarting `nginx` you should be good to go!

If you run into some `nginx` configuration problems, check the error logs to see what could be going wrong. One thing that I ran into was
my server name was too long and this gave me some server hash name error. I resolved this by adding the line 
`server_names_hash_bucket_size 128;` to my `nginx` config file here `/etc/nginx/nginx.conf`. 

There are a bunch of ways to deploy a flask app on a server so oyou don't have to do this. I just found this to be the fastest way. For
reference [this](http://exploreflask.com/en/latest/deployment.html) is the guide I followed, it's pretty detailed.
