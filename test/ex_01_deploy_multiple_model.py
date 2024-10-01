import ray
from ray import serve

# The code snippet provided is using Ray Serve, which is a scalable and versatile library for building
# and deploying machine learning models and other Python functions as web services. Here is a
# breakdown of the code:
# ray.init()

# serve.start()


# @serve.deployment(route_prefix='/test_1')
# class test_1:
#     def __init__(self, *args, **kwargs):
#         print("test_1")

@serve.deployment
class test:
    def __init__(self):
        print("test_2")
        
# app_1 = test_1.options(name='test_1').bind()
for i in range(0,4):
    app = test.options().bind()
    route_prefix = f'/test_{i}'
    name=f'test_{i}'
    serve.run(app, route_prefix=route_prefix, name=name)   
    
print(serve.status())