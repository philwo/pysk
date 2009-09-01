# -*- coding: utf-8 -*-
# * encoding: utf-8 *

import decimal
import re

from reportlab.pdfgen		import canvas
from reportlab.lib.units	import cm, mm
from reportlab.lib.pagesizes	import A4, portrait, landscape


class PyCPDF( canvas.Canvas ):
	def __init__( self, fileobj, orientation='P' ):
		pg = { 'P': portrait, 'L': landscape };
		canvas.Canvas.__init__( self, fileobj, pagesize=pg[orientation](A4) );
		
		# Adobe Reader behaved awkwardly when text was on a page without a Font having been set, so let's be sure about that
		self.setFont( "Helvetica", 12 );
		self.setFillColorRGB( 0, 0, 0 );
		
		self.margin      = [ 10*mm, 20*mm ];
		self.lineheight  = 7*mm;
		self.pos         = [ self.margin[0], self.pageheight - self.margin[1] - self.lineheight ];
		self.textColor   = [ 0, 0, 0 ];
		self.bgColor     = [ 1, 1, 1 ];
		self.borderColor = [ 0, 0, 0 ];
		self.autoFill    = False;
		self.fillLine    = False;
		self.orientation = orientation;
		
		self.setBgColorRGB( 224, 235, 255 );
	
	remainingSpace  = property( lambda self: self.pagewidth  - self.margin[0] - self.pos[0], None );
	remainingHeight = property( lambda self: self.pos[1] - self.margin[1],                   None );
	
	# this method shall be compatible with TCPDF's cell(), except height being unspecified means "use the default" instead of 0.
	# http://www.tecnick.com/pagefiles/tcpdf/doc/com-tecnick-tcpdf/TCPDF.html#methodCell
	def cell( self, width=None, height=None, txt='', border=False, ln=False, align='L', fill=False, link=None, stretch=0 ):
		if width is None or width > self.remainingSpace:
			width  = self.remainingSpace;
		
		if height is None:
			height = self.lineheight;
		
		if self.autoFill:
			fill = fill or self.fillLine;
		
		if border or fill:
			# We need to draw a rectangle, either for background or border.
			if fill:
				self.setFillColorRGB( *self.bgColor );
			if border:
				self.setStrokeColorRGB( *self.borderColor );
			
			self.rect( self.pos[0], self.pos[1]-height+self.lineheight-2*mm, width, height, border, fill );
		
		if txt:
			self.setFillColorRGB( *self.textColor );
			if   align == 'L':
				self.drawString(        self.pos[0]+1*mm,       self.pos[1], txt );
			elif align == 'R':
				self.drawRightString(   self.pos[0]+width-1*mm, self.pos[1], txt );
			elif align == 'C':
				self.drawCentredString( self.pos[0]+width/2.0,  self.pos[1], txt );
		
		if link:
			#print "ich linke mal auf %s" % link;
			self.linkURL(
				link,
				( self.pos[0],       self.pos[1]+self.lineheight-height-2*mm,     # Lower left corner
				  self.pos[0]+width, self.pos[1]+self.lineheight                  # Upper right corner
				  )
				);
		
		self.pos[0] += width;
		
		if ln:
			self.ln( height );
	
	def img( self, file, width=None, height=None, align="n", link=None, **kwargs ):
		w, h = self.drawImage( file,
			self.pos[0], self.pos[1] + self.lineheight - height,
			width=width, height=height,
			preserveAspectRatio=True,
			**kwargs
			);
		if link:
			self.linkURL(
				link,
				( self.pos[0],       self.pos[1]+self.lineheight-height-2*mm,     # Lower left corner
				  self.pos[0]+width, self.pos[1]+self.lineheight                  # Upper right corner
				  )
				);
		return w, h;
	
	def row( self, height=None, border=True, fill=False ):
		if border:
			count = 1;
			for cell in self.cellData:
				if 'txt' in cell and len( cell['txt'] ) > count:
					count = len( cell['txt'] );
			if height is None:
				height = self.lineheight;
			for cell in self.cellData:
				self.cell(
					width  = cell['width'],
					height = height * count,
					# border = True,
					fill   = fill,
					);
			self.ln(0);
		
		while not self.dictempty( self.cellData ):
			for cell in self.cellData:
				if 'txt' in cell and cell['txt']:
					txt = unicode( cell['txt'].pop(0) );
				else:
					txt = '';
				
				mycell = cell.copy();
				mycell['txt']    = txt;
				mycell['fill']   = fill if not border else False;
				
				self.cell( **mycell );
				
			if fill and not border and self.remainingSpace > 0:
				self.cell( fill=True );
			
			self.ln();
	
	
	def goto( self, x = None, y = None ):
		if x is None:
			x = self.margin[0];
		if y is None:
			y = self.pageheight - self.margin[1];
		
		if   x == -1:
			self.pos[1] = y;
		elif y == -1:
			self.pos[0] = x;
		else:
			self.pos = [x, y];
	
	def ln( self, height=None ):
		if self.autoFill:
			self.fillLine = not self.fillLine;
		if height is None:
			height = self.lineheight;
		self.pos[1] -= height;
		self.pos[0]  = self.margin[0];
	
	
	def showPage( self, **kwargs ):
		canvas.Canvas.showPage( self, **kwargs );
		#self.pos = self.margin;
		self.pos = [ self.margin[0], self.pageheight - self.margin[1] ];
	
	pagewidth  = property( lambda self: self._pagesize[0], None );
	pageheight = property( lambda self: self._pagesize[1], None );
	
	def setTextColorRGB( self, r=0, g=0, b=0 ):
		self.textColor = [ r/255.0, g/255.0, b/255.0 ];
	
	def setBgColorRGB( self, r=0, g=0, b=0 ):
		self.bgColor = [ r/255.0, g/255.0, b/255.0 ];
	
	def setBorderColorRGB( self, r=0, g=0, b=0 ):
		self.borderColor = [ r/255.0, g/255.0, b/255.0 ];
	
	def splitSentence( self, sentence ):
		# Replace currently existing - by ~ so they survive the splitting
		allwords  = sentence.replace( '-', '~' ).split(' ');
		syllables = [];
		
		for word in allwords:
			# split the word into syllables, replace back the ~ and add the syllables list to the list
			# of words which will be returned.
			syllables.append( [ syll.replace( '~', '-' ) for syll in self.splitSyllables( word ) ] );
		
		return syllables;
	
	def splitSyllables( self, word ):
		vowels     = "aeiouöäüAEIOUÖÄÜ";
		consonants = "bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ";
		
		regexes = ( (
				"([%s]){1}(sch|ch|ck|st|ß|[%s]{1})([%s]{1})"                  % ( vowels, consonants, vowels ),
				r"\1-\2\3",
			), (
				"([%s]){1}(sch|ch|ck|st|ß|[%s]{1})(sch|ch|ck|st|ß|[%s]{1,})"  % ( vowels, consonants, consonants ),
				r"\1\2-\3",
			), (
				"-(.){1}([^\wöäüßÖÄÜ]+)",                                      # remove end syllables with a single char
				r"\1\2",
			), (
				"-(.){1}([^%s]+[^\wöäüßÖÄÜ]+)" % vowels,                       # remove end syllables without consonants
				r"\1\2",
			) );
		
		for regex, replace in regexes:
			rgx  = re.compile( regex );
			word = rgx.sub( replace, word );
		
		return word.split( '-' );
	
	
	def splitByLength( self, fieldData, width ):
		cellData = [];
		
		if self.stringWidth( fieldData ) > width:
			wordlist = self.splitSentence(fieldData);
			fieldData = '';
			for word in wordlist:
				# word is a list of syllables
				fullword = ''.join(word);
				
				if self.stringWidth( fieldData + fullword ) <= width:
					fieldData += fullword + ' ';
				else:
					for syllable in word:
						# If this syllable will not fill up the line, or will fill up any line
						# by itself (so breaking  won't help anything), just add it
						# splitSyllables sort of epic failed in the latter case...
						if    self.stringWidth( fieldData + syllable ) <= width \
						   or self.stringWidth( syllable ) > width:
							fieldData += syllable;
						else:
							# Check if this is the first syllable. if it is, the last word
							# that was printed filled up the line, so we simply need to add
							# a linebreak, but not print a -.
							if syllable is not word[0]:
								fieldData += '-';
							cellData.append( fieldData );
							fieldData = syllable;
					fieldData += ' ';
				
				if word is wordlist[-1]:	# Last word in sentence
					cellData.append( fieldData );
					fieldData = '';
		else:
			cellData.append( fieldData );
		return cellData;
	
	def dictempty( self, dict ):
		for item in dict:
			if 'txt' in item and item['txt']:
				return False;
		return True;
	
	












