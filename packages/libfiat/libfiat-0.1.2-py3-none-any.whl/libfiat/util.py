# Copyright (C) 2024 Daniel Page <dan@phoo.org>
#
# Use of this source code is restricted per the MIT license, a copy of which 
# can be found via https://opensource.org/license/mit (and which is included 
# as LICENSE.txt within the associated archive or repository).

import abc, enum

from libfiat import driver
from libfiat import util

# =============================================================================

class Req( enum.IntEnum ) :
  """ An enumeration 
      that captures
      request     message tags (or identifiers).
  """

  PING            = ord( '!' )
  RESET           = ord( '*' )
  VERSION         = ord( '$' )

  NAMEOF          = ord( '"' )
  SIZEOF          = ord( '|' )
  USEDOF          = ord( '#' )
  TYPEOF          = ord( '?' )

  WR              = ord( '>' )
  RD              = ord( '<' )

  KERNEL          = ord( '=' )
  KERNEL_PROLOGUE = ord( '[' )
  KERNEL_EPILOGUE = ord( ']' )

class Ack( enum.IntEnum ) :
  """ An enumeration 
      that captures
      acknowledge message tags (or identifiers).
  """

  SUCCESS         = ord( '+' )
  FAILURE         = ord( '-' )

class  Type( int ) :
  """ A "rich" type
      that captures (otherwise integer)
      a register  type.
  """

  LENGTH_FIX      = 0x0
  LENGTH_VAR      = 0x1

  def     wr( self ) :
    return ( self >> 0 ) & 0x1
  def     rd( self ) :
    return ( self >> 1 ) & 0x1
  def length( self ) :
    return ( self >> 2 ) & 0x1

class Index( int ) :
  """ A "rich" type
      that captures (otherwise integer)
      a register index.
  """

  def is_spr( self ) :
    """Test whether the index refers to a special-purpose register (or SPR)."""
    return     ( self & 0x80 )
  def is_gpr( self ) :
    """Test whether the index refers to a general-purpose register (or GPR)."""
    return not ( self & 0x80 )

  def   addr( self ) :
    """Extract the address field of the index."""
    return     ( self & 0x7F )

# =============================================================================
