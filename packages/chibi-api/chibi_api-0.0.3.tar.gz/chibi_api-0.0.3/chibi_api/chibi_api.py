# -*- coding: utf-8 -*-
from chibi_requests import Chibi_url, Response
from chibi_hybrid import Class_property


class Chibi_inner_api( Chibi_url ):
    response = None

    def __getattr__( self, name ):
        try:
            return super().__getattribute__( name )
        except AttributeError:
            result = self._build_url( name )
            return result

    def solve_response( self, method, response ):
        if self.response:
            new_class = self.response.get( method, None )
            if new_class is None:
                return response
            if not isinstance( new_class, type ):
                raise NotImplementedError(
                    "se espera que la clase <{new_class}> sea una clase"
                )
            if not issubclass( new_class, Response ):
                raise NotImplementedError(
                    "no esta implementado el uso de tipos "
                    f"<{type(new_class)}> se esperaba un <{Response}>"
                )
            else:
                return new_class.from_response( response )
        else:
            return response

    def _build_url( self, name, *args, **kw ):
        """
        contrulle la url del api, cuando tiene una autentifacion
        se la pasa a la nueva url
        """
        result = type( self )( self, parent=self, **kw ) + name
        if self.auth:
            result += self.auth
        return result

    def get( self, *args, **kw ):
        result = super().get( *args, **kw )
        result = self.solve_response( 'get', result )
        return result

    def post( self, *args, **kw ):
        result = super().post( *args, **kw )
        result = self.solve_response( 'post', result )
        return result

    def delete( self, *args, **kw ):
        result = super().delete( *args, **kw )
        result = self.solve_response( 'delete', result )
        return result

    def put( self, *args, **kw ):
        result = super().put( *args, **kw )
        result = self.solve_response( 'put', result )
        return result

    def create( self, *args, **kw ):
        """
        create es una alias de post
        """
        return self.post( *args, json=kw )


class Chibi_api( Chibi_url ):
    schema = 'http'
    host = None
    inner_api_class = None

    def __new__( cls, *args, **kw ):
        if cls.host is None:
            raise NotImplementedError
        if cls.schema is None:
            raise NotImplementedError
        if not args:
            obj = super().__new__( cls, f'{cls.schema}://{cls.host}', **kw )
        else:
            obj = super().__new__( cls, *args, **kw )

        if not cls.inner_api_class:
            obj._API = Chibi_inner_api( obj, parent=obj )
        else:
            obj._API = cls.inner_api_class( obj, parent=obj )
        return obj

    @Class_property
    def API( cls ):
        instance = cls()
        return instance.API

    @API.instance
    def API( self ):
        return self._API
