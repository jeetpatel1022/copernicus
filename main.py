import endpoints
from google.appengine.ext import ndb
from protorpc import remote

from endpoints_proto_datastore.ndb import EndpointsModel

class MyModel(EndpointsModel):

  attr1 = ndb.StringProperty()
  attr2 = ndb.StringProperty()
  created = ndb.DateTimeProperty(auto_now_add=True)
  owner = ndb.UserProperty()

class LabTest(EndpointsModel):
  ldl = ndb.StringProperty()
  hdl = ndb.StringProperty()
  hbac = ndb.StringProperty()


class VisitModel(EndpointsModel):
  lipids = ndb.StringProperty()
  hbac = ndb.StringProperty()
  visitdate = ndb.DateTimeProperty(auto_now_add=True)
  owner = ndb.UserProperty()
  verify = ndb.StringProperty()

class PhysicianModel(EndpointsModel):
  fname = ndb.StringProperty()
  lname = ndb.StringProperty()
  npi = ndb.StringProperty()
  specialty = ndb.StringProperty()
  # vcode = ndb.StringProperty() Need to add reference to allow admins to set
  # vmultiplier = ndb.StringProperty()



@endpoints.api(name='myapi', version='v1', description='My Little API',
               audiences=[endpoints.API_EXPLORER_CLIENT_ID])
class MyApi(remote.Service):
  @MyModel.method(user_required=True,
                  path='mymodel', http_method='POST', name='mymodel.insert')
  def MyModelInsert(self, my_model):
    my_model.owner = endpoints.get_current_user()

    my_model.put()
    return my_model

  @MyModel.query_method(user_required=True,
                        path='mymodels', name='mymodel.list')
  def MyModelList(self, query):

    return query.filter(MyModel.owner == endpoints.get_current_user())

@endpoints.api(name='copernicus', version='v1', description="First version API", audiences=[endpoints.API_EXPLORER_CLIENT_ID])
class CopernicusApi(remote.Service):
  @VisitModel.method(user_required=True, path='visitmodel', http_method='POST', name='visitmodel.insert')
  def VisitModelInsert(self, visit_model):
    visit_model.owner = endpoints.get_current_user()

    visit_model.put()
    return visit_model

  @VisitModel.query_method(user_required=True, path='visits', name='visit.list')
  def VisitModelList(self, query):
    return query.filter(VisitModel.owner == endpoints.get_current_user())

application = endpoints.api_server([MyApi, CopernicusApi], restricted=False)