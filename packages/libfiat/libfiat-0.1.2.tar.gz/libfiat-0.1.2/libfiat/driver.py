# Copyright (C) 2024 Daniel Page <dan@phoo.org>
#
# Use of this source code is restricted per the MIT license, a copy of which 
# can be found via https://opensource.org/license/mit (and which is included 
# as LICENSE.txt within the associated archive or repository).

import abc, enum

from libfiat import driver
from libfiat import util

# =============================================================================

class DriverAbs( abc.ABC ) :
  def __init__( self, device = None ) :
    self.device = device

# -----------------------------------------------------------------------------

class DriverImpBinary( DriverAbs ) :
  def __init__( self, device = None ) :
    super().__init__( device = device )

  def    _flush( self    ) :
    self.device.flush()

  def   _req_wr( self, x ) :
    self.device.write( bytes( [ int( x ) ] ) )
  
  def   _req_rd( self    ) :
    return util.Req( int.from_bytes( self.device.read( 1 ), 'little' ) )
  
  def   _ack_wr( self, x ) :
    self.device.write( bytes( [ int( x ) ] ) )
  
  def   _ack_rd( self    ) :
    return util.Ack( int.from_bytes( self.device.read( 1 ), 'little' ) )
  
  def  _byte_wr( self, x ) :
    self.device.write( bytes( [ int( x ) ] ) )
  
  def  _byte_rd( self    ) :
    return      int.from_bytes( self.device.read( 1 ), 'little' )
  
  def  _vint_wr( self, x ) :
    while ( True ) :
      t = x & 0x7F ; x >>= 7
    
      if ( x ) :
        self.device.write( bytes( [ t | 0x80 ] ) )
      else :
        self.device.write( bytes( [ t | 0x00 ] ) ) ; break
    
  def  _vint_rd( self    ) :
    r = 0 ; n = 0
  
    while ( True ) :
      t = int.from_bytes( self.device.read( 1 ), 'little' ) ; r |= ( t & 0x7F ) << n ; n += 7
  
      if ( not ( t & 0x80 ) ) :
        break
  
    return r
  
  def  _data_wr( self, x ) :
    self._vint_wr( len( x ) ) ; self.device.write( x )
  
  def  _data_rd( self    ) :
    size = self._vint_rd() ; return self.device.read( size )
  
  def ping( self ) :
    # ->
    self._req_wr( int( util.Req.PING ) )
    # --
    self._flush()
    # <-
    ack = self._ack_rd()
    # ==
    return ( ack, )

  def reset( self ) :
    # ->
    self._req_wr( int( util.Req.RESET ) )
    # --
    self._flush()
    # <-
    ack = self._ack_rd()
    # ==
    return ( ack, )

  def version( self ) :
    # ->
    self._req_wr( int( util.Req.VERSION ) )
    # --
    self._flush()
    # <-
    ack = self._ack_rd() ; patch = self._byte_rd() ; minor = self._byte_rd() ; major = self._byte_rd()
    # ==
    return ( ack, patch, minor, major )

  def nameof( self, index ) :
    # ->
    self._req_wr( int( util.Req.NAMEOF ) ) ; self._byte_wr( index )
    # --
    self._flush()
    # <-
    ack = self._ack_rd() ; name = self._data_rd().decode()
    # ==
    return ( ack, name )

  def sizeof( self, index ) :
    # ->
    self._req_wr( int( util.Req.SIZEOF ) ) ; self._byte_wr( index )
    # --
    self._flush()
    # <-
    ack = self._ack_rd() ; size =            self._vint_rd()
    # ==
    return ( ack, size )

  def usedof( self, index ) :
    # ->
    self._req_wr( int( util.Req.USEDOF ) ) ; self._byte_wr( index )
    # --
    self._flush()
    # <-
    ack = self._ack_rd() ; used =            self._vint_rd()
    # ==
    return ( ack, used )

  def typeof( self, index ) :
    # ->
    self._req_wr( int( util.Req.TYPEOF ) ) ; self._byte_wr( index )
    # --
    self._flush()
    # <-
    ack = self._ack_rd() ; type = util.Type( self._byte_rd() )
    # ==
    return ( ack, type )

  def wr( self, index, data ) :
    # ->
    self._req_wr( int( util.Req.WR ) ) ; self._byte_wr( index ) ; self._data_wr( data )
    # --
    self._flush()
    # <-
    ack = self._ack_rd()
    # ==
    return ( ack, )

  def rd( self, index       ) :
    # ->
    self._req_wr( int( util.Req.RD ) ) ; self._byte_wr( index )
    # --
    self._flush()
    # <-
    ack = self._ack_rd() ; data = self._data_rd()
    # ==
    return ( ack, data )

  def kernel         ( self, op, rep ) :
    # ->
    self._req_wr( int( util.Req.KERNEL          ) ) ; self._byte_wr( op ) ; self._vint_wr( rep )
    # --
    self._flush()
    # <-
    ack = self._ack_rd()
    # ==
    return ( ack, )

  def kernel_prologue( self, op      ) :
    # ->
    self._req_wr( int( util.Req.KERNEL_PROLOGUE ) ) ; self._byte_wr( op )
    # --
    self._flush()
    # <-
    ack = self._ack_rd()
    # ==
    return ( ack, )

  def kernel_epilogue( self, op      ) :
    # ->
    self._req_wr( int( util.Req.KERNEL_EPILOGUE ) ) ; self._byte_wr( op )
    # --
    self._flush()
    # <-
    ack = self._ack_rd()
    # ==
    return ( ack, )

# -----------------------------------------------------------------------------

class DriverImpText( DriverAbs ) :
  def __init__( self, device = None ) :
    super().__init__( device = device )

  def    _flush( self    ) :
    self.device.flush()

  def  _byte_wr( self, x ) :
    r  = '{0:1X}'.format( ( x >> 4 ) & 0xF )
    r += '{0:1X}'.format( ( x >> 0 ) & 0xF )

    return r
  
  def  _byte_rd( self, x ) :
    if ( len( x ) == 2 ) :
      r  = int( x[ 0 ], 16 ) << 4
      r += int( x[ 1 ], 16 ) << 0

      return r

    else :
      return 0
  
  def  _vint_wr( self, x ) :
    r = ''

    while ( True ) :
      t = x & 0x7F ; x >>= 7
    
      if ( x ) :
        r += self._byte_wr( t | 0x80 )
      else :
        r += self._byte_wr( t | 0x00 ) ; break

    return r
    
  def  _vint_rd( self, x ) :
    r = 0 ; n = 0
  
    while ( True ) :
      t = self._byte_rd( x[ 0 : 2 ] ) ; x = x[ 2 : ] ; r |= ( t & 0x7F ) << n ; n += 7
  
      if ( not ( t & 0x80 ) ) :
        break
  
    return r

  def  _data_wr( self, x ) :
    return bytes.hex( x )

  def  _data_rd( self, x ) :
    return bytes.fromhex( x )

  def  _line_wr( self, x ) :
    for t in ( x + '\x0D' ) :
      self.device.write( t.encode( 'ascii' ) ) ; self.device.flush()
    
  def  _line_rd( self    ) :  
    r = ''
    
    while( True ):
      t = self.device.read( 1 ).decode( 'ascii' )
        
      if ( t == '\x0D' ) :
        break
      else :
        r += t

    return r

  def   _decode( self, x ) :
    x = x.strip().split( ' ' ) 

    if ( len( x ) > 0 ) :
      ack = util.Ack.FAILURE if ( x[ 0 ] == '-' ) else util.Ack.SUCCESS
    else :
      ack = util.Ack.FAILURE

    if ( len( x ) > 1 ) :
      tok = x[ 1 : ]
    else :
      tok = list()

    return ( ack, tok )

  def ping( self ) :
    # ->
    self._line_wr( chr( util.Req.PING ) )
    # --
    self._flush()
    # <-
    ( ack, tok ) = self._decode( self._line_rd() )
    # ==
    return ( ack, )

  def reset( self ) :
    # ->
    self._line_wr( chr( util.Req.RESET ) )
    # --
    self._flush()
    # <-
    ( ack, tok ) = self._decode( self._line_rd() )
    # ==
    return ( ack, )

  def version( self ) :
    # ->
    self._line_wr( chr( util.Req.VERSION ) )
    # --
    self._flush()
    # <-
    ( ack, tok ) = self._decode( self._line_rd() ) ; patch = int( self._byte_rd( tok[ 0 ] ) ) ; minor = int( self._byte_rd( tok[ 1 ] ) ) ; major = int( self._byte_rd( tok[ 2 ] ) )
    # ==
    return ( ack, patch, minor, major )

  def nameof( self, index ) :
    # ->
    self._line_wr( chr( util.Req.NAMEOF ) + ' ' + self._byte_wr( index ) )
    # --
    self._flush()
    # <-
    ( ack, tok ) = self._decode( self._line_rd() ) ; size = self._vint_rd( tok[ 0 ] ) ; name = self._data_rd( tok[ 1 ] ).decode()
    # ==
    return ( ack, name )

  def sizeof( self, index ) :
    # ->
    self._line_wr( chr( util.Req.SIZEOF ) + ' ' + self._byte_wr( index ) )
    # --
    self._flush()
    # <-
    ( ack, tok ) = self._decode( self._line_rd() ) ; size =          ( self._vint_rd( tok[ 0 ] ) )
    # ==
    return ( ack, size )

  def usedof( self, index ) :
    # ->
    self._line_wr( chr( util.Req.USEDOF ) + ' ' + self._byte_wr( index ) )
    # --
    self._flush()
    # <-
    ( ack, tok ) = self._decode( self._line_rd() ) ; used =          ( self._vint_rd( tok[ 0 ] ) )
    # ==
    return ( ack, used )

  def typeof( self, index ) :
    # ->
    self._line_wr( chr( util.Req.TYPEOF ) + ' ' + self._byte_wr( index ) )
    # --
    self._flush()
    # <-
    ( ack, tok ) = self._decode( self._line_rd() ) ; type = util.Type( self._byte_rd( tok[ 0 ] ) )
    # ==
    return ( ack, type )

  def wr( self, index, data ) :
    # ->
    self._line_wr( chr( util.Req.WR ) + ' ' + self._byte_wr( index ) + ' ' + self._vint_wr( len( data ) ) + ' ' + self._data_wr( data ) )
    # --
    self._flush()
    # <-
    ( ack, tok ) = self._decode( self._line_rd() )
    # ==
    return ( ack, )

  def rd( self, index       ) :
    # ->
    self._line_wr( chr( util.Req.RD ) + ' ' + self._byte_wr( index ) )
    # --
    self._flush()
    # <-
    ( ack, tok ) = self._decode( self._line_rd() ) ; size = self._vint_rd( tok[ 0 ] ) ; data = self._data_rd( tok[ 1 ] )
    # ==
    return ( ack, data )

  def kernel         ( self, op, rep ) :
    # ->
    self._line_wr( chr( util.Req.KERNEL          ) + ' ' + self._byte_wr( op ) + ' ' + self._vint_wr( rep ) )
    # --
    self._flush()
    # <-
    ( ack, tok ) = self._decode( self._line_rd() )
    # ==
    return ( ack, )

  def kernel_prologue( self, op      ) :
    # ->
    self._line_wr( chr( util.Req.KERNEL_PROLOGUE ) + ' ' + self._byte_wr( op ) )
    # --
    self._flush()
    # <-
    ( ack, tok ) = self._decode( self._line_rd() )
    # ==
    return ( ack, )

  def kernel_epilogue( self, op      ) :
    # ->
    self._line_wr( chr( util.Req.KERNEL_EPILOGUE ) + ' ' + self._byte_wr( op ) )
    # --
    self._flush()
    # <-
    ( ack, tok ) = self._decode( self._line_rd() )
    # ==
    return ( ack, )

# =============================================================================
