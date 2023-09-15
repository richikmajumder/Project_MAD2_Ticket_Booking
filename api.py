from flask import Flask, request, jsonify, send_file, render_template_string, url_for
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager, jwt_required, create_access_token,get_jwt_identity,get_jwt
from flask_bcrypt import Bcrypt
from datetime import datetime,timedelta
from flask_cors import CORS
from functools import wraps
from mail import send_email_reminder,send_monthly_report,send_ticket_png,send_email_with_attachment,generate_qr,compress_image,send_monthly_report_pdf,report_pdf
from models import db, Venue, Show, Link, User, Booking, Rating, PasswordResetToken
from flask_caching import Cache
from celery import Celery
from celery.schedules import crontab
from tzlocal import get_localzone
from email.message import EmailMessage
import ssl,smtplib,os,random,string,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "your_secret_key"  # Set your own secret key
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SECRET_KEY"] = "secret"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)
app.config["JWT_ALGORITHM"] = "HS512"
app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_HOST'] = '127.0.0.1'#'redis-18646.c15.us-east-1-2.ec2.cloud.redislabs.com'
app.config['CACHE_REDIS_PORT'] = 6379#18646
#app.config['CACHE_REDIS_PASSWORD'] = '3bG5vfT5F7brHuj9HcQ15a9g7H3Wrx2P'
app.config['CACHE_REDIS_DB'] = 0
app.config["CELERY_BROKER_URL"]='redis://127.0.0.1:6379/0'
app.config['result_backend']='redis://127.0.0.1:6379/0'
app.config["timezone"] = str(get_localzone())
celery = Celery(app.name, broker=app.config["CELERY_BROKER_URL"])
celery.conf.update(app.config)
os.environ["timezone"] = str(get_localzone())

jwt = JWTManager(app)
api = Api(app)
cors = CORS(app)
cache = Cache(app)
bcrypt = Bcrypt(app)
db.init_app(app)
with app.app_context():
  db.create_all()



@jwt.expired_token_loader
def expired_token_callback(expired_token,payload):
    # Custom response for expired token
    return jsonify({'message': 'Token has expired'}), 401

@jwt.invalid_token_loader
def invalid_token_callback(invalid_token):
  return jsonify({"message":"Token is invalid"}),401

@jwt.unauthorized_loader
def missing_token_callback(error):
    # Custom response for missing token
    return jsonify({"message": "Token is missing"}), 401

def roles_required(*required_roles):    
  def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
      #user_role = request.headers.get('Role')
      if get_jwt().get('is_admin')==0:
        user_role='user'
      elif get_jwt().get('is_admin')==1:
        user_role='admin'
      else:
        user_role=None
      if user_role not in required_roles:
        return {'message': 'Access denied'}, 403
      return func(*args, **kwargs)
    return wrapper
  return decorator

def make_cache_key(*args, **kwargs):
  # Generate a unique cache key based on the request URL and input parameters
  cache_key = f"{request.url}-{request.args}"
  return cache_key

def string_to_date(date):
  return datetime.strptime(date,'%Y-%m-%d').date()

def string_to_time(time):
  if len(time)==5:
    return datetime.strptime(time,'%H:%M').time()
  elif len(time)==8:
    return datetime.strptime(time[:-3],'%H:%M').time()

def get_current_datetime():
  """now_utc = datetime.utcnow()
  local_timezone = pytz.timezone('Asia/Calcutta')
  now_local = now_utc.replace(tzinfo=pytz.utc).astimezone(local_timezone)
  return now_local"""
  return datetime.now()

def request_args():
  return len(request.args)>0 or request.headers.get('cache')=="off"

def generate_token():
  domain=string.ascii_letters+string.digits
  token=''
  for i in range(128):
    token+=random.choice(domain)
  return token

def format_date(date):
  new_date=str(date)
  new_date=datetime.strptime(new_date,"%Y-%m-%d")
  new_date=datetime.strftime(new_date,"%a, %b %d")
  return new_date

def format_time(time):
  new_time=str(time)
  new_time=datetime.strptime(new_time,"%H:%M:%S")
  new_time=datetime.strftime(new_time,"%I:%M %p")
  return new_time

# Sign up resource
class SignupResource(Resource):
  def post(self):
    username = request.json.get("username")
    email = request.json.get("email")
    password = request.json.get("password")
    firstname = request.json.get("firstname")
    lastname = request.json.get("lastname")
    pdf_report = request.json.get("pdf_report")
    # Check if username is already taken
    if User.query.filter_by(username=username,email=email).first():
      return {"message": "Username already taken"}, 400
    # Create new user
    new_user = User(username=username,email=email,firstname=firstname,lastname=lastname,password=bcrypt.generate_password_hash(password),pdf_report=pdf_report)
    db.session.add(new_user)
    db.session.commit()
    return {"message": "User created successfully"}, 201
# Sign in resource
class SigninResource(Resource):
  def post(self):
    username = request.json.get("username")
    password = request.json.get("password")
    # Check if username and password are valid
    user = User.query.filter_by(username=username).first()
    if not user:
      user =  User.query.filter_by(email=username).first()
    if user and bcrypt.check_password_hash(user.password,password):
      user.last_login = get_current_datetime()
      db.session.commit()
      # Generate access token
      access_token = create_access_token(identity=user.username,additional_claims={"email":user.email,"is_admin":user.is_admin})
      if user.is_admin:
        return {"access_token":access_token,"role":"admin"}, 200
      return {"access_token":access_token,"role":"user"}, 200
    elif user and not bcrypt.check_password_hash(user.password,password):
      return {"message": "Incorrect password"}, 401
    elif not user:
      return {"message":"User not found"},401   
# Protected resource
class AdminProtectedResource(Resource):
  @jwt_required()
  @roles_required("admin")  
  def get(self):
    current_user = get_jwt_identity()
    email = get_jwt().get("email")
    return {"username": current_user, "email": email}, 200

class UserProtectedResource(Resource):
  @jwt_required()
  @roles_required("user")  
  def get(self):
    current_user = get_jwt_identity()
    email = get_jwt().get("email")
    return {"username": current_user, "email": email}, 200

class UsernameCheck(Resource):
  def get(self,username):
    user=User.query.filter_by(username=username).first()
    print(User.query.all())
    if user:
      return True
    return False

class EmailCheck(Resource):
  def get(self,email):
    email=User.query.filter_by(email=email).first()
    if email:
      return True
    return False

class ShowCheck(Resource):
  def get(self,show):
    show_=Show.query.filter(Show.name.ilike(show)).first()
    if show_:
      return {"message":True,"name":show_.name}
    return {"message":False}

class AdminSignup(Resource):
  def post(self):
    username = request.json.get("username")
    email = request.json.get("email")
    password = request.json.get("password")
    firstname = request.json.get("firstname")
    lastname = request.json.get("lastname")
    # Check if username is already taken
    if User.query.filter_by(username=username,email=email).first():
      return {"message": "Username already taken"}, 400
    # Create new user
    new_user = User(username=username,email=email,firstname=firstname,lastname=lastname,password=bcrypt.generate_password_hash(password),is_admin=True)
    db.session.add(new_user)
    db.session.commit()
    return {"message": "User created successfully"}, 201

class Venues(Resource):
  @jwt_required()
  @roles_required("admin")
  def post(self):
    print("post",request.json)
    venue_name=request.json.get("venuename")
    venue_place=request.json.get("place")
    venue_location=request.json.get("location")
    venue_capacity=request.json.get("capacity")
    existing_venue=Venue.query.filter_by(name=venue_name,place=venue_place,location=venue_location,capacity=venue_capacity).first()
    if existing_venue:
      print(existing_venue.name)
      return {"message":"Venue already present"},200
    new_venue = Venue(name=venue_name, place=venue_place, location=venue_location, capacity=venue_capacity)
    db.session.add(new_venue)
    db.session.commit()
    return {"message":"Venue added successfully"},200


  #@cache.cached(make_cache_key=make_cache_key,timeout=5,unless=request_args)
  def get(self):
    if len(request.args) == 0:
      print("nill",request.headers.get('cache'))
      venues=Venue.query.all()
      venue_list=[]
      for venue in venues:
        venue_list.append({"id":venue.id,"name":venue.name,"place":venue.place,"location":venue.location,"capacity":venue.capacity,"Modifier":False})
      return jsonify(venue_list)
    elif len(request.args) != 0:
      try: 
        id = request.args.get("id")
        venue = Venue.query.get(id)
        links = []
        if venue:
          if len(venue.link)>=1:
            #venue_link=Link.query.filter_by(venue_id=id).order_by(Link.date,Link.time).all()
            for link in venue.link:
              show = Show.query.get(link.show_id)
              links.append({"id":link.id,"show_name":show.name,"rating":show.rating,"tags":show.tags,"date":format_date(link.date),"time":format_time(link.time),"ticket_price":link.ticket_price,"show_id":link.show_id,"venue_id":link.venue_id,"Modifier":False})
            return jsonify({"links":links,"venue":{"id":venue.id,"name":venue.name,"place":venue.place,"location":venue.location,"capacity":venue.capacity}})
          return jsonify({"venue":{"id":venue.id,"name":venue.name,"place":venue.place,"location":venue.location,"capacity":venue.capacity}})
        return {"msg":"Venue not found"}
      except:
        return {"msg":"Something went wrong"}

  @jwt_required()
  @roles_required("admin")  
  def patch(self):
    print("patch",request.json)
    print("patch",request.json["name"],request.json["place"],request.json["location"],request.json["capacity"],request.json["id"])
    Venue.query.filter_by(id=request.json["id"]).update(dict(name=request.json["name"],place=request.json["place"],location=request.json["location"],capacity=request.json["capacity"]))
    db.session.commit()
    print("updated")
    return {"msg":"updated"}

  @jwt_required()
  @roles_required("admin")  
  def delete(self,id):
    #print("delete",request.json)
    venue=Venue.query.get(id)
    if venue:
      #if venue.name==request.json['name'] and venue.place==request.json['place'] and venue.location==request.json['location'] and venue.capacity==request.json['capacity']:
      db.session.delete(venue)
      db.session.commit()
      return {"message":"Deleted successfully"},200
      #return {"message":"Something went wrong"}  
      return {"message":"Venue not found"}
    
class Shows(Resource):
  @jwt_required()
  @roles_required("admin")  
  def post(self):
    print(request.json)
    capacity=Venue.query.get(request.json.get("venue_id")).capacity
    if not Show.query.filter_by(name=request.json.get("name")).first():      
      show=Show(name=request.json.get("name"),rating=request.json.get("rating"),tags=request.json.get("tags"))
      print(1)
      db.session.add(show)
      db.session.commit()
      if not Link.query.filter_by(venue_id=request.json.get("venue_id"),show_id=show.id,date=string_to_date(request.json.get("date")),time=string_to_time(request.json.get("time"))).first():
        link=Link(venue_id=request.json.get("venue_id"),show_id=show.id,date=string_to_date(request.json.get("date")),time=string_to_time(request.json.get("time")),ticket_price=request.json.get("price"),tickets_left=capacity)
        db.session.add(link)
        db.session.commit()
        return {"message":"Show added successfully"},200
      else:
        return {"message":"Something went wrong."}
    elif not Link.query.filter_by(venue_id=request.json.get("venue_id"),show_id=Show.query.filter_by(name=request.json.get("name")).first().id,date=string_to_date(request.json.get("date")),time=string_to_time(request.json.get("time"))).first():
      link=Link(venue_id=request.json.get("venue_id"),show_id=Show.query.filter_by(name=request.json.get("name")).first().id,date=string_to_date(request.json.get("date")),time=string_to_time(request.json.get("time")),ticket_price=request.json.get("price"),tickets_left=capacity)
      db.session.add(link)
      db.session.commit()
      return {"message":"Show is already present. It has been linked to the venue successfully"},200
    else:
      return {"message":"Show is already linked to the selected venue for the given date & time"},200
  
  #@cache.cached(make_cache_key=make_cache_key,timeout=5,unless=request_args)
  def get(self):
    if len(request.args)==0:
      shows=Show.query.all()
      showlist=[]
      for show in shows:
        showlist.append({"id":show.id,"name":show.name,"tags":show.tags,"rating":show.rating,"Modifier":False})
      print(showlist)
      return jsonify(showlist)
    elif len(request.args)!=0:
      try:
        id = request.args.get('id')
        show = Show.query.get(id)
        links = []
        if show:
          if len(show.link)>=1:
            show_link=Link.query.filter_by(show_id=id).order_by(Link.date,Link.time).all()
            for link in show_link:
              venue = Venue.query.get(link.venue_id)
              links.append({"id":link.id,"venue_id":link.venue_id,"show_id":link.show_id,"venue_name":venue.name,"venue_place":venue.place,"venue_location":venue.location,"capacity":venue.capacity,"date":format_date(link.date),"time":format_time(link.time),"ticket_price":link.ticket_price,"Modifier":False})
            return jsonify({"links":links,"show":{"id":show.id,"name":show.name,"rating":show.rating,"tags":show.tags}})
          return jsonify({"show":{"id":show.id,"name":show.name,"rating":show.rating,"tags":show.tags},"message":"Show is not linked to any venue"})
        return {"message":"Show not found"}
      except:
        return {"message":"Something went wrong"}
  
  @jwt_required()
  @roles_required("admin")
  def patch(self):
    print("patch",request.json)
    Show.query.filter_by(id=request.json['id']).update(dict(name=request.json['name'],tags=request.json['tags'],rating=request.json['rating']))
    db.session.commit()
    print("updated")
    return {"message":"Updated"}

  @jwt_required()
  @roles_required("admin")
  def delete(self,id):
    #print("delete",request.json)
    #show=Show.query.filter_by(id=request.json['id'],name=request.json['name'],rating=request.json['rating'],tags=request.json['tags']).delete()
    show=Show.query.get(id)
    print(show)
    if show:
      #if show.name==request.json['name'] and show.rating==request.json['rating'] and show.tags==request.json['tags']:            
      db.session.delete(show)
      db.session.commit()
      return {"message":"Show deleted"},200
    #return {"message":"Something went wrong"}
    return {"message":"Show not found"}

class ShowLink(Resource):
  @jwt_required()
  @roles_required("admin")
  def delete(self,id):
    #print("delete ShowLink",request.json)
    link=Link.query.get(id)
    if link:
      #if format_date(link.date)==request.json['date'] and format_time(link.time)==request.json['time'] and link.venue_id==request.json['venue_id'] and link.show_id==request.json['show_id']:
      db.session.delete(link)
      db.session.commit()
      return {"message":"Show delinked successfully"},200
    #return {"message":"Something went wrong"}
    return {"message":"Link is missing"}

  def get(self):
    link = Link.query.get(request.args.get('id'))
    if link:
      venue = Venue.query.get(link.venue_id)
      if venue:
        return jsonify({"id":link.id,"show_id":link.show_id,"venue_id":link.venue_id,"venue_name":venue.name,"venue_place":venue.place,"venue_location":venue.location,"venue_capacity":venue.capacity,"date":format_date(link.date),"time":format_time(link.time),"ticket_price":link.ticket_price})
      return {"message":"No venues found"}
    return {"message":"Link is missing"}

  @jwt_required()
  @roles_required("admin")
  def patch(self):
    print(request.json)
    link = Link.query.filter_by(id=request.json['id'],show_id=request.json['show_id'],venue_id=request.json['venue_id'],date=string_to_date(request.json['date']),time=string_to_time(request.json['time']),ticket_price=request.json['price']).first()
    if link:
      return {"message":"Duplicate entry or entry unchanged"}
    else:
      Link.query.filter_by(id=request.json['id'],show_id=request.json['show_id'],venue_id=request.json['venue_id']).update(dict(date=string_to_date(request.json['date']),time=string_to_time(request.json['time']),ticket_price=request.json['price']))
      db.session.commit()
      return {"message":"Updated successfully"}

class VenueLink(Resource):
  @jwt_required()
  @roles_required("admin")
  def delete(self,id):
    #print("delete VenueLink",request.json)
    link=Link.query.get(id)
    if link:
      #if format_date(link.date)==request.json['date'] and format_time(link.time)==request.json['time'] and link.venue_id==request.json['venue_id'] and link.show_id==request.json['show_id']:        
      db.session.delete(link)
      db.session.commit()
      return {"message":"Show delinked successfully"},200
    #return {"message":"Something went wrong"}
    return {"message":"Link is missing"}
    
  def get(self):
    link = Link.query.get(request.args.get('id'))
    if link:
      show = Show.query.get(link.show_id)
      if show:
        return jsonify({"id":link.id,"venue_id":link.venue_id,"show_id":link.show_id,"show_name":show.name,"rating":show.rating,"tags":show.tags,"date":format_date(link.date),"time":format_time(link.time),"ticket_price":link.ticket_price})
      return {"message":"No shows found"}
    return {"message":"Link is missing"}

  @jwt_required()
  @roles_required("admin")
  def patch(self):
    print(request.json)
    link = Link.query.filter_by(id=request.json['id'],show_id=request.json['show_id'],venue_id=request.json['venue_id'],date=string_to_date(request.json['date']),time=string_to_time(request.json['time']),ticket_price=request.json['price']).first()
    if link:
      return {"message":"Duplicate entry or entry unchanged"}
    else:
      Link.query.filter_by(id=request.json['id'],show_id=request.json['show_id'],venue_id=request.json['venue_id']).update(dict(date=string_to_date(request.json['date']),time=string_to_time(request.json['time']),ticket_price=request.json['price']))
      db.session.commit()
      return {"message":"Updated successfully"}

class Search(Resource):
  @cache.cached(make_cache_key=make_cache_key,timeout=10)
  def get(self):
    query=request.args.get('query')
    venue_name=Venue.query.filter(Venue.name.contains(query)).all()
    venue_location=Venue.query.filter(Venue.location.contains(query)).all()
    show_name=Show.query.filter(Show.name.contains(query)).all()
    search_list=[]
    if venue_name:
      for venue in venue_name:
        d={"name":venue.name,"place":venue.place,"location":venue.location,"capacity":venue.capacity,"type":"Venue name","result":venue.name+' '+venue.place+', '+venue.location,"venue_id":venue.id,"link":[]}
        links=Link.query.filter_by(venue_id=venue.id).filter(Link.date>=datetime.now().date()).order_by(Link.date,Link.time).all()
        if links:
          for link in links:
            show=Show.query.get(link.show_id)
            d["link"].append({"link_id":link.id,"show_id":link.show_id,"date":format_date(link.date),"time":format_time(link.time),"ticket_price":link.ticket_price,"tickets_left":link.tickets_left,"show_name":show.name,"rating":show.rating,"tags":show.tags})
        search_list.append(d)
    if venue_location:
      for venue in venue_location:
        d={"name":venue.name,"place":venue.place,"location":venue.location,"capacity":venue.capacity,"type":"Location","result":venue.name+' '+venue.place+', '+venue.location,"venue_id":venue.id,"link":[]}
        links=Link.query.filter_by(venue_id=venue.id).filter(Link.date>=datetime.now().date()).order_by(Link.date,Link.time).all()
        if links:
          for link in links:
            show=Show.query.get(link.show_id)
            d["link"].append({"link_id":link.id,"show_id":link.show_id,"date":format_date(link.date),"time":format_time(link.time),"ticket_price":link.ticket_price,"tickets_left":link.tickets_left,"show_name":show.name,"rating":show.rating,"tags":show.tags})
        search_list.append(d)
    if show_name:
      for show in show_name:
        d={"name":show.name,"tags":show.tags,"rating":show.rating,"type":"Show name","result":show.name,"show_id":show.id,"link":[]}
        links=Link.query.filter_by(show_id=show.id).filter(Link.date>=datetime.now().date()).order_by(Link.date,Link.time).all()
        if links:
          for link in links:
            venue=Venue.query.get(link.venue_id)
            d["link"].append({"link_id":link.id,"venue_id":link.venue_id,"date":format_date(link.date),"time":format_time(link.time),"ticket_price":link.ticket_price,"tickets_left":link.tickets_left,"venue_name":venue.name,"place":venue.place,"location":venue.location})
        search_list.append(d)
    return jsonify(search_list)

class Bookings(Resource):
  @jwt_required()
  @roles_required('user')
  def get(self):
    if not (len(request.args)):
      venues = Venue.query.all()
      data=[]
      for venue in venues:
        details={"id":venue.id,"name":venue.name,"place":venue.place,"location":venue.location,"modifier":False,"links":[]}
        ordered_link=Link.query.filter_by(venue_id=venue.id).filter(Link.date>=datetime.now().date()).order_by(Link.date,Link.time).all()
        for link in ordered_link:
          details['links'].append({"id":link.id,"show_id":link.show_id,"date":str(link.date),"time":str(link.time),"ticket_price":link.ticket_price,"tickets_left":link.tickets_left,"show_name":Show.query.get(link.show_id).name})
        data.append(details)
      #print(data)
      return jsonify(data)
    elif request.args.get('id'):
      id=request.args.get('id')
      link=Link.query.get(id)
      user=User.query.filter_by(username=get_jwt_identity()).first()
      wallet=None
      if link: 
        ticket_price=link.ticket_price
        venue=Venue.query.get(link.venue_id)
        show=Show.query.get(link.show_id)
        if link.tickets_left<=int(0.9*venue.capacity) and link.tickets_left>int(0.8*venue.capacity):
          ticket_price*=1.1
        elif link.tickets_left<=int(0.8*venue.capacity) and link.tickets_left>int(0.7*venue.capacity):
          ticket_price*=1.2
        elif link.tickets_left<=int(0.7*venue.capacity) and link.tickets_left>int(0.6*venue.capacity):
          ticket_price*=1.3
        elif link.tickets_left<=int(0.6*venue.capacity) and link.tickets_left>int(0.5*venue.capacity):
          ticket_price*=1.4
        elif link.tickets_left<=int(0.5*venue.capacity) and link.tickets_left>int(0.4*venue.capacity):
          ticket_price*=1.5  
        elif link.tickets_left<=int(0.4*venue.capacity) and link.tickets_left>int(0.3*venue.capacity):
          ticket_price*=1.6
        elif link.tickets_left<=int(0.3*venue.capacity) and link.tickets_left>int(0.2*venue.capacity):
          ticket_price*=1.7
        elif link.tickets_left<=int(0.2*venue.capacity) and link.tickets_left>int(0.1*venue.capacity):
          ticket_price*=1.8
        elif link.tickets_left<=int(0.1*venue.capacity) and link.tickets_left>0:
          ticket_price*=1.9
        if user:
          print(user.wallet)
          wallet=user.wallet
          if wallet!=None and wallet>=0:
            return jsonify({"id":link.id,"show_name":show.name,"venue_name":venue.name,"place":venue.place,"location":venue.location,"ticket_price":int(ticket_price),"date":str(link.date),"time":str(link.time),"tickets_left":link.tickets_left,"wallet":wallet,"price":link.ticket_price})  
        return jsonify({"id":link.id,"show_name":show.name,"venue_name":venue.name,"place":venue.place,"location":venue.location,"ticket_price":int(ticket_price),"date":str(link.date),"time":str(link.time),"tickets_left":link.tickets_left,"price":link.ticket_price})
      return {"message":"Details not found"},402
    return {"message":"Something went wrong"}

  @jwt_required()
  @roles_required('user')
  def post(self):
    print(request.json)
    user=User.query.filter_by(username=get_jwt_identity()).first()
    user_id=user.id
    link=Link.query.get(request.json.get('id'))
    if user_id and link:
      check=request.json.get('checked')
      if check:
        balance=request.json.get('wallet')
        if balance!=None and balance>0 and balance==user.wallet:
          user.wallet=max(0,user.wallet-request.json.get('ticket_price')*request.json.get('no_of_seats_requested'))
      if link.date<datetime.now().date():
        return {"message":"Bookings for this show is already closed"}
      booking=Booking(user_id=user_id,link_id=request.json.get('id'),venue_id=link.venue_id,show_id=link.show_id,tickets_booked=request.json.get('no_of_seats_requested'),ticket_price=request.json.get('ticket_price'),date=get_current_datetime().date())
      db.session.add(booking)
      Link.query.filter_by(id=request.json.get('id')).update(dict(tickets_left=link.tickets_left-request.json.get('no_of_seats_requested')))
      db.session.commit()
      file=open('templates/Ticket.html','r')
      data=file.read()
      file.close()
      venue=booking.venue.name+' '+booking.venue.place+', '+booking.venue.location
      html=render_template_string(data,venue=venue,show_name=booking.show.name,date=str(link.date),time=str(link.time),tickets_booked=request.json.get('no_of_seats_requested'),price_paid=request.json.get('ticket_price')*request.json.get('no_of_seats_requested'))
      send_booking_confirmation.delay(user.email,html,dict(venue=venue,show_name=booking.show.name,date=str(link.date),time=str(link.time)[0:-3],tickets_booked=request.json.get('no_of_seats_requested'),price_paid=request.json.get('ticket_price')*request.json.get('no_of_seats_requested'),user=user.firstname+' '+user.lastname))
      return {"message":"Tickets booked successfully. \n A confirmation email will be sent shortly."}
    return {"message":"Something went wrong"}

class BookingHistory(Resource):
  @jwt_required()
  @roles_required('user')
  def get(self):
    if request.args.get('id'):
      user_id=User.query.filter_by(username=request.args.get('id')).first().id
      bookings=Booking.query.filter_by(user_id=user_id)
      details=[]
      for booking in bookings:
        id=booking.id
        print(booking.show.name)
        show_name=booking.show.name
        venue_name=booking.venue.name
        place=booking.venue.place
        location=booking.venue.location
        link_id=booking.link_id
        date=format_date(Link.query.get(link_id).date)
        time=format_time(Link.query.get(link_id).time)
        tickets_booked=booking.tickets_booked
        ticket_price=booking.ticket_price
        rating=Rating.query.filter_by(user_id=booking.user_id,show_id=booking.show_id).first()
        if rating:
          rating=rating.rating
        else:
          rating=None
        details.append({"id":id,"show_name":show_name,"venue_name":venue_name,"place":place,"location":location,"link_id":link_id,"date":date,"time":time,"tickets_booked":tickets_booked,"ticket_price":ticket_price,"rating":rating,"show_id":booking.show.id,"user_id":user_id,"modifier":False})
      return jsonify(details)

  @jwt_required()
  @roles_required('user')
  def post(self):
    print(request.json)
    if not Rating.query.filter_by(user_id=request.json.get('user_id'),show_id=request.json.get('show_id')).first():
      user_rating=Rating(user_id=request.json.get('user_id'),show_id=request.json.get('show_id'),rating=request.json.get('rating'))
      db.session.add(user_rating)
      db.session.commit()
      total=0
      count=0
      ratings=Rating.query.filter_by(show_id=request.json.get('show_id')).all()
      for rating in ratings:
        total+=rating.rating
        count+=1
      show=Show.query.get(request.json.get('show_id'))
      show.rating=total/count
      db.session.commit()
    return {"message":"Rating updated successfully"}

class ExportVenue(Resource):
  @jwt_required()
  @roles_required('admin')
  def post(self):
    print(request.json)
    user=User.query.filter_by(username=request.json.get('username')).first()
    venue=Venue.query.get(request.json.get('venue_id'))
    tickets_booked=0
    price=0
    if venue:
      for booking in venue.booking:
        tickets_booked+=booking.tickets_booked
        price+=booking.ticket_price*booking.tickets_booked
    text=f"Name of venue,No of shows,No of bookings,No of tickets booked,Revenue (in Rs)\n{venue.name} {venue.place} {venue.location},{len(venue.link)},{len(venue.booking)},{tickets_booked},{price}"
    file=open("files/ExportedVenue.csv",'w')
    file.write(text),file.close()
    type='csv'
    subject="Exported venue details"
    body=f"Hello {user.firstname},\n Your file is ready for download. \nKindly look for 'ExportedVenue.csv' in the attachment section."
    receiver_email=user.email
    sender_email=open('email.txt','r').readline()
    password=open('password.txt','r').readline()
    send_email.delay(sender_email,receiver_email,subject,body,password,'files/ExportedVenue.csv',type)
    print(venue.booking)
    return {"message":"You will receive an email in your registered email shortly"}

class Profile(Resource):
  @jwt_required()
  @roles_required('user','admin')
  def get(self):
    username=request.args.get('username')
    user=User.query.filter_by(username=username).first()
    return jsonify({"first_name":user.firstname,"last_name":user.lastname,"email":user.email,"id":user.id,"admin":user.is_admin,"pdf_report":user.pdf_report})
  
  @jwt_required()
  @roles_required('user','admin')
  def patch(self):
    print(request.json)
    username=request.json.get('username')
    if request.json.get("pdf_report") in [True,False]:
      if request.json.get("password"):
        user=User.query.filter_by(username=username).update(dict(firstname=request.json.get('first_name'),lastname=request.json.get('last_name'),password=bcrypt.generate_password_hash(request.json.get('password')),pdf_report=request.json.get("pdf_report")))
      else:
        user=User.query.filter_by(username=username).update(dict(firstname=request.json.get('first_name'),lastname=request.json.get('last_name'),pdf_report=request.json.get("pdf_report")))
      db.session.commit()
    else:
      if request.json.get("password"):
            user=User.query.filter_by(username=username).update(dict(firstname=request.json.get('first_name'),lastname=request.json.get('last_name'),password=bcrypt.generate_password_hash(request.json.get('password')),pdf_report=request.json.get("pdf_report")))
      else:
        user=User.query.filter_by(username=username).update(dict(firstname=request.json.get('first_name'),lastname=request.json.get('last_name'),pdf_report=request.json.get("pdf_report")))
      db.session.commit()
    print('Job done')
    return {"message":"Profile updated successfully"}

class Stats(Resource):
  @jwt_required()
  @roles_required('admin','user')
  def get(self):
    if request.args.get('name')=='venue':
      venues=Venue.query.all()
      venue_list=[venue.name+' '+venue.place+', '+venue.location for venue in venues]
      revenue=[]
      for venue in venues:
        total=0
        for booking in venue.booking:
          total+=booking.tickets_booked*booking.ticket_price
        revenue.append(total)
      plt.bar(venue_list,revenue,width=0.1)
      plt.xlabel('Name of venue',color='red')
      plt.ylabel('Revenue generated in ₹',color='red')
      plt.xticks(rotation=90)
      plt.tight_layout()
      plt.savefig('files/venues.png')
      plt.close()
      return send_file('files/venues.png',mimetype='image/png')

    elif request.args.get('name')=='show':
      shows=Show.query.all()
      show_list=[show.name for show in shows]
      revenue=[]
      total_tickets_booked=[]
      for show in shows:
        total=0
        tickets_booked=0
        for booking in show.booking:
          total+=booking.tickets_booked*booking.ticket_price
          tickets_booked+=booking.tickets_booked
        revenue.append(total)
        total_tickets_booked.append(tickets_booked)
      
      # Plot the bar chart for number of bookings
      fig, ax1 = plt.subplots()
      ax1.bar(show_list, total_tickets_booked, color='b', alpha=0.5)
      ax1.set_ylabel('Number of tickets sold', color='b')
      ax1.tick_params(axis='y', labelcolor='b')

      # Create a second y-axis for total revenue
      ax2 = ax1.twinx()
      ax2.plot(show_list, revenue, color='r', marker='o')
      ax2.set_ylabel('Total Revenue', color='r')
      ax2.tick_params(axis='y', labelcolor='r')

      # Set labels and title
      ax1.set_xlabel('Shows')  # Set the x-label for ax1
      plt.title('Number of Tickets sold and Total Revenue for Shows')
      plt.savefig('files/shows.png')
      plt.close()
      return send_file('files/shows.png',mimetype='image/png')

    elif request.args.get('name')=='popular':
      shows=Show.query.all()
      show_list=[show.name for show in shows]
      total_tickets_booked=[]
      for show in shows:
        tickets_booked=0
        for booking in show.booking:
          tickets_booked+=booking.tickets_booked
        total_tickets_booked.append(tickets_booked)

      plt.bar(show_list,total_tickets_booked,width=0.1)
      plt.xlabel('Name of show',color='red')
      plt.ylabel('Total tickets booked',color='red')
      plt.xticks(rotation=90)
      plt.tight_layout()
      plt.savefig('files/trending_show.png')
      plt.close()
      return send_file('files/trending_show.png',mimetype='image/png')

class Wallet(Resource):
  @jwt_required()
  @roles_required('user')
  def get(self):
    username=request.args.get('username')
    return User.query.filter_by(username=username).first().wallet
  
  @jwt_required()
  @roles_required('user')
  def patch(self):
    print(request.json)
    add_money=request.json.get('add_money')
    username=request.json.get('username')
    user=User.query.filter_by(username=username).first()
    if add_money==0:
      user.wallet=add_money
      db.session.commit()
      return {"message":"Wallet activated successfully"}
    elif add_money>0 and add_money<=10000:
      user.wallet+=add_money
      if user.wallet>10000:
        db.session.rollback()
        return {"message":"Sorry! Your wallet can't hold more than ₹10,000/-"}
      elif user.wallet>=0 and user.wallet<=10000:
        db.session.commit()
        return {"message":"Funds loaded successfully"}
    else:
      return {"message":"Something went wrong"}

class ForgotPassword(Resource):
  def post(self):
    email=request.json.get('email')
    user=User.query.filter_by(email=email).first()
    if user:
      token=generate_token()
      expiry=datetime.now()+timedelta(hours=1)
      reset_token=PasswordResetToken.query.filter_by(user_id=user.id).all()
      if reset_token:
        for token_ in reset_token:
          db.session.delete(token_)
      ResetToken=PasswordResetToken(user_id=user.id,token=token,validity=expiry)
      db.session.add(ResetToken)
      db.session.commit()
      url = 'http://127.0.0.1:8081'
      url += url_for('resetpassword',token=token)#_external=True
      print(url)
      send_password_reset_link.delay(email,url)
      return {"message":"Kindly check your email for password reset link"}
    return {"message":"User not found"}

class ResetPassword(Resource):
  def post(self):
    username=request.json.get('username')   
    password=request.json.get('password')
    token=request.json.get('token')
    password_reset_token=PasswordResetToken.query.filter_by(token=token).first()
    if password_reset_token:
      if password_reset_token.validity>=datetime.now():
        user=User.query.get(password_reset_token.user_id)
        if user.username==username:
          user.password=bcrypt.generate_password_hash(password)
          db.session.delete(password_reset_token)
          db.session.commit()
          return {"message":"Password updated successfully"}
        return {"message":"Username mismatch"}
      db.session.delete(password_reset_token)
      db.session.commit()
      return {"message":"Password reset link expired"}
    return {"message":"Invalid link"}


  def get(self,token):
    resetToken=PasswordResetToken.query.filter_by(token=token).first()
    if resetToken:
      if resetToken.validity>=datetime.now():
        return {"message":"Token valid"}
      return {"message":"Token expired"}
    return {"message":"Invalid token"}

class TokenVerifier(Resource):
  @jwt_required()
  @roles_required("user","admin")
  def get(self):
    role=get_jwt().get('is_admin')
    if role:
      role='admin'
      return {"role":role}
    return {"role":"user"}


@celery.task
def send_email(sender_email,receiver_email,subject,body,password,file,filetype):
  send_email_with_attachment(sender_email,receiver_email,subject,body,password,file,filetype)
  print("Exported data sent successfully")


@celery.task
def send_password_reset_link(receiver,url):
  sender=open('email.txt','r').readline()
  password=open('password.txt','r').readline()
  subject="Password Reset Link"
  body=f"Click on the following link to reset your password: {url}"
  send_email_reminder(sender,receiver,subject,body,password)
  print("Reset link sent")


@celery.task
def send_booking_confirmation(receiver,content,data):
  sender=open('email.txt','r').readline()
  password=open('password.txt','r').readline()
  subject="Booking confirmation"
  body="Congratulations! Your ticket is now booked.\n  Kindly bring the hard/soft copy of the ticket attached in this email.\n Thank you for booking with us."
  file='files/ticket.png'
  filetype='png'
  generate_qr(data)
  send_ticket_png(content)
  compress_image(file,file)  
  send_email_with_attachment(sender,receiver,subject,body,password,file,filetype)
  print("Ticket booking confirmation email sent successfully")


@celery.task
def send_reminder():
  with app.app_context():
    users=User.query.all()
  now=datetime.now()+timedelta(days=2) #now is day after tommorrow for demonstration
  yesterday=now-timedelta(days=1) #Yesterday is tommorrow
  sender=open('email.txt','r').readline()
  password=open('password.txt','r').readline()
  subject="🎉 Let's Reignite the Fun! Your Ticket Booking Adventure Awaits 🎫"
  
  for user in users:
    body=f"""
Hey there, {user.firstname}! 👋

We miss you! It's been a day since we last saw you at Ticketing, and we can't help but wonder what incredible movies you're missing out on! 🌟
See you there! 🎉

Cheers,
The Ticketing app Team 🎟️🎆"""
    if user.last_login<yesterday and not user.is_admin:
      send_email_reminder(sender,user.email,subject,body,password)
  print("Done")


@celery.task
def send_entertainment_report():
  with app.app_context():
    users = User.query.filter(User.is_admin==False).all()
    now = datetime.now()+timedelta(days=30)
    start_date = (now.replace(day=1)-timedelta(days=1)).replace(day=1).date()
    end_date = (now.replace(day=1)-timedelta(days=1)).date()
    monthYear = (now.replace(day=1)-timedelta(days=1)).replace(day=1).strftime('%B %Y')
    mailing_list={}
    pdf_mailing_list={}
    if users:
      for user in users:
        name = user.firstname + ' ' + user.lastname
        bookings = Booking.query.join(Link).filter(Booking.user_id==user.id,Booking.date.between(start_date, end_date)).all()
        show_date = Booking.query.join(Link).with_entities(Booking.id,Link.date.label('ShowDate'),Link.time.label('ShowTime')).filter(Booking.user_id==user.id,Booking.date.between(start_date, end_date)).all()
        total_spend = sum(booking.tickets_booked * booking.ticket_price for booking in bookings)
        ratings = Rating.query.filter_by(user_id=user.id).all()
        tags = {}
        for booking in bookings:
          if booking.show.tags not in tags.keys():
            tags[booking.show.tags] = 1
          else:
            tags[booking.show.tags] += 1        
        mini=0
        genre=''
        for tag in tags.keys():
          if tags[tag]>=mini:
            mini=tags[tag]
            genre=tag

        if bookings:
          f=open('templates/Monthly Entertainment Report.html')
          file=f.read()
          if user.pdf_report==False:
            mailing_list[user.email]=render_template_string(file,monthYear=monthYear,bookings=bookings,show_date=show_date,name=name,username=user.username,total_spend=total_spend,ratings=ratings,genre=genre).replace('\n','').replace('\"','')
          elif user.pdf_report:
            pdf_mailing_list[user.email]=render_template_string(file,monthYear=monthYear,bookings=bookings,show_date=show_date,name=name,username=user.username,total_spend=total_spend,ratings=ratings,genre=genre).replace('\n','').replace('\"','')
          f.close()    
      
      for email in mailing_list.keys():
        sender=open('email.txt','r').readline()
        password=open('password.txt','r').readline()
        send_monthly_report(sender,email,'Monthly Report',mailing_list[email],password)
      
      for email in pdf_mailing_list.keys():
        sender=open('email.txt','r').readline()
        password=open('password.txt','r').readline()
        report_pdf(pdf_mailing_list[email])
        send_monthly_report_pdf(sender,email,'files/Report.pdf',password)
      print('Task complete')



celery.conf.beat_schedule = {
  'send_reminder': {
    'task': 'api.send_reminder',
    'schedule': crontab(hour=20, minute=7, day_of_week='*'),
    'args': (),
    'kwargs': {},
    'options': {
      'tz': 'Asia/Kolkata',
    }
  },
  'send_entertainment_report': {
    'task': 'api.send_entertainment_report',
    'schedule':crontab(hour=21, minute=51),
    'options':{
      'tz': 'Asia/Kolkata'
    }
  }
}


# Add resources to the API
api.add_resource(SignupResource, "/signup")
api.add_resource(SigninResource, "/signin")
api.add_resource(AdminProtectedResource, "/protected")
api.add_resource(UserProtectedResource, "/user/protected")
api.add_resource(UsernameCheck, "/api/username/<username>")
api.add_resource(EmailCheck, "/api/email/<email>")
api.add_resource(ShowCheck, "/api/show/<show>")
api.add_resource(AdminSignup,"/api/admin/signup")
api.add_resource(Venues,"/api/venue","/api/venue/delete/<id>")
api.add_resource(Shows,"/api/show","/api/show/delete/<id>")
api.add_resource(ShowLink,"/api/admin/showlink/delink/<id>","/api/admin/showlink")
api.add_resource(VenueLink,"/api/admin/venuelink/delink/<id>","/api/admin/venuelink")
api.add_resource(Search,"/api/search")
api.add_resource(Bookings,"/api/book")
api.add_resource(BookingHistory,"/api/bookinghistory")
api.add_resource(ExportVenue,"/api/venue/export")
api.add_resource(Profile,"/api/profile")
api.add_resource(Stats,"/api/stats")
api.add_resource(Wallet,"/api/wallet")
api.add_resource(ForgotPassword,"/api/forgot/password")
api.add_resource(ResetPassword,"/api/reset/password","/api/reset/password/<token>")
api.add_resource(TokenVerifier,"/api/token/verifier")

if __name__ == "__main__":
  app.run(debug=True,port=8080)

  