from pydantic import BaseModel, Extra
import json

class Base(BaseModel):
    class Config:
         validate_assignment = True
        #  extra = Extra.forbid
    def __getattribute__(self, prop):
        val = super(Base, self).__getattribute__(prop)
        # __root__ is a custom pydantic thing 
        if hasattr(val, '__root__'):
            return str(val.__root__)
        else:
            return val

    
    def jsonld(self, **kwargs):
        ### approach 1 - fails because .json() returns a string
        # return {"@context": "http://iiif.io/api/presentation/3/context.json", **self.json(**kwargs)}
        
        ### approach 2 - using the extra argument in Config. fails because it adds both @context and context to the bottom of the serialisation
        # self.context = "http://iiif.io/api/presentation/3/context.json"
        # return self.json(by_alias=True, **kwargs)
        
        ### approach 3 - kludge the context onto the start of the string. works, but doesn't respect indent settings etc
        # json_str = self.json(**kwargs)
        # return '{"@context": "http://iiif.io/api/presentation/3/context.json",' + json_str[1:]

        ### approach 4 - use the pydantic .dict() function to get the dict, add the context at the top and dump it to json - fails because you can't pass the pydantic arguments so get all the null values
        # return json.dumps({"@context": "http://iiif.io/api/presentation/3/context.json", **self.dict()}, **kwargs)

        ### approach 5 - use pydantic to render json, reparse it, add the context and re-dump with modified kwargs - works but it's a bit messy
        # new_dict = {"@context": "http://iiif.io/api/presentation/3/context.json", **json.loads(self.json(**kwargs))}
        # pydantic_args = ["include", "exclude", "by_alias", "exclude_unset", "exclude_defaults", "exclude_none", "encoder"]
        # for arg in pydantic_args:
        #     try:
        #         del(kwargs[arg])
        #     except KeyError:
        #         pass
        # return json.dumps(new_dict, **kwargs)

        ### approach 6- use the pydantic .dict() function to get the dict with pydantic options, add the context at the top and dump to json with modified kwargs
        pydantic_args = ["include", "exclude", "by_alias", "exclude_unset", "exclude_defaults", "exclude_none", "encoder"]
        dict_kwargs = dict([(arg, kwargs[arg]) for arg in kwargs.keys() if arg in pydantic_args])
        json_kwargs = dict([(arg, kwargs[arg]) for arg in kwargs.keys() if arg not in pydantic_args])
        return json.dumps({"@context": "http://iiif.io/api/presentation/3/context.json", **self.dict(**dict_kwargs)}, **json_kwargs)

    
    def jsonld_dict(self, **kwargs):
        pydantic_args = ["include", "exclude", "by_alias", "exclude_unset", "exclude_defaults", "exclude_none", "encoder"]
        dict_kwargs = dict([(arg, kwargs[arg]) for arg in kwargs.keys() if arg in pydantic_args])
        return {"@context": "http://iiif.io/api/presentation/3/context.json", **self.dict(**dict_kwargs)}