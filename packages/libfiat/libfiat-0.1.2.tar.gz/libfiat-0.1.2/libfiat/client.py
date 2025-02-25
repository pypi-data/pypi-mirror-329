# Copyright (C) 2024 Daniel Page <dan@phoo.org>
#
# Use of this source code is restricted per the MIT license, a copy of which 
# can be found via https://opensource.org/license/mit (and which is included 
# as LICENSE.txt within the associated archive or repository).

import abc, enum, serial, socket

from libfiat import driver
from libfiat import util

# =============================================================================

class ClientAbs( abc.ABC ) :
  """ A class
      that captures
      generic 
      client-side communication,
      over either binary or text protocol.
  """

  def __init__( self, driver = 'binary' ) :
    self.device     =   None

    self.driver     = driver
    self.driver_imp =   None

  def ping ( self ) :
    if ( self.driver_imp == None ) :
      raise Exception()      

    return self.driver_imp.ping ()

  def reset( self ) :
    if ( self.driver_imp == None ) :
      raise Exception()      

    return self.driver_imp.reset()

  def version( self ) :
    if ( self.driver_imp == None ) :
      raise Exception()      

    return self.driver_imp.version()

  def nameof( self, index ) :
    if ( self.driver_imp == None ) :
      raise Exception()      

    return self.driver_imp.nameof( index )

  def sizeof( self, index ) :
    if ( self.driver_imp == None ) :
      raise Exception()      

    return self.driver_imp.sizeof( index )

  def usedof( self, index ) :
    if ( self.driver_imp == None ) :
      raise Exception()      

    return self.driver_imp.usedof( index )

  def typeof( self, index ) :
    if ( self.driver_imp == None ) :
      raise Exception()      

    return self.driver_imp.typeof( index )

  def wr( self, index, data ) :
    if ( self.driver_imp == None ) :
      raise Exception()      

    return self.driver_imp.wr( index, data )

  def rd( self, index       ) :
    if ( self.driver_imp == None ) :
      raise Exception()      

    return self.driver_imp.rd( index       )

  def kernel         ( self, op = 0, rep = 1 ) :
    if ( self.driver_imp == None ) :
      raise Exception()      

    return self.driver_imp.kernel         ( op, rep )

  def kernel_prologue( self, op = 0          ) :
    if ( self.driver_imp == None ) :
      raise Exception()      

    return self.driver_imp.kernel_prologue( op      )

  def kernel_epilogue( self, op = 0          ) :
    if ( self.driver_imp == None ) :
      raise Exception()      

    return self.driver_imp.kernel_epilogue( op      )

# -----------------------------------------------------------------------------

class ClientImpSocket( ClientAbs ) :
  """ A (sub-)class
      that captures
      socket-based (e.g., via network, or loopback connection)
      client-side communication,
      over either binary or text protocol.
  """

  def __init__( self, driver = 'binary' ) :
    super().__init__( driver = driver )

  def  open( self, host, port, **args ) :
    if ( self.device != None ) :
      self.device.close()

    t = socket.socket( socket.AF_INET, socket.SOCK_STREAM ) ; t.connect( ( host, port ) ) ; self.device = t.makefile( mode = 'rwb', buffering = 1024 )

    if   ( self.driver == 'binary' ) :
      self.driver_imp = driver.DriverImpBinary( device = self.device )
    elif ( self.driver == 'text'   ) :
      self.driver_imp = driver.DriverImpText  ( device = self.device )
    else :
      raise Exception()      

  def close( self ) :
    if ( self.device != None ) :
      self.device.close()

# -----------------------------------------------------------------------------

class ClientImpSerial( ClientAbs ) :
  """ A (sub-)class
      that captures
      serial-based (i.e., via UART) 
      client-side communication,
      over either binary or text protocol.
  """

  def __init__( self, driver = 'binary' ) :
    super().__init__( driver = driver )

  def  open( self,       port, **args ) :
    if ( self.device != None ) :
      self.device.close()
 
    self.device = serial.Serial( port = port, **args )

    if   ( self.driver == 'binary' ) :
      self.driver_imp = driver.DriverImpBinary( device = self.device )
    elif ( self.driver == 'text'   ) :
      self.driver_imp = driver.DriverImpText  ( device = self.device )
    else :
      raise Exception()      
  
  def close( self ) :
    if ( self.device != None ) :
      self.device.close()

# =============================================================================
