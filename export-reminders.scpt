JsOsaDAS1.001.00bplist00�Vscripto� / /   s e t   t h i n g s   u p 
 v a r   a p p   =   A p p l i c a t i o n ( ' R e m i n d e r s ' ) ; 
 a p p . i n c l u d e S t a n d a r d A d d i t i o n s   =   t r u e ; 
 
 / /   c h o o s e   l i s t 
 v a r   l i s t N a m e   =   a p p . c h o o s e F r o m L i s t ( a p p . l i s t s . n a m e ( ) ,   {   w i t h P r o m p t :   " W h i c h   L i s t ? "   } ) ; 
 i f   ( l i s t N a m e )   { 
 
 	 / /   g e t   t h e   d a t a   f r o m   t h e   l i s t 
 	 v a r   r e m i n d e r s L i s t   =   a p p . l i s t s . b y N a m e ( l i s t N a m e ) . r e m i n d e r s ; 
 	 v a r   l i s t N a m e s   =   r e m i n d e r s L i s t . n a m e ( ) ; 
 	 v a r   l i s t C o m p l e t e d   =   r e m i n d e r s L i s t . c o m p l e t e d ( ) ; 
 	 v a r   l i s t D u e D a t e s   =   r e m i n d e r s L i s t . d u e D a t e ( ) ; 
 	 v a r   l i s t B o d i e s   =   r e m i n d e r s L i s t . b o d y ( ) ; 
 	 
 	 / /   c r e a t e   a   s i n g l e   a r r a y 
 	 v a r   l i s t   =   [ ] ; 
 	 f o r ( v a r   i = 0 ;   i < l i s t N a m e s . l e n g t h ;   i + + )   { 
 	 	 l i s t . p u s h ( { n a m e :   l i s t N a m e s [ i ] ,   c o m p l e t e d :   l i s t C o m p l e t e d [ i ] ,   d u e D a t e :   l i s t D u e D a t e s [ i ] ,   b o d y :   l i s t B o d i e s [ i ] } ) ; 
 	 } 
 	 
 	 / /   s o r t   t h e   l i s t 
 	 / / l i s t . s o r t ( ( a ,   b )   = >   ( a . n a m e   >   b . n a m e ) ) ; 
 	 / / l i s t . s o r t ( ( a ,   b )   = >   ( a . d u e D a t e   >   b . d u e D a t e ) ) ; 
 
 	 / /   b u i l d   t e x t   f r o m   l i s t 
 	 v a r   t e x t   =   " " ; 
 	 v a r   n   =   0 ; 
 	 f o r ( v a r   i = 0 ;   i < l i s t . l e n g t h ;   i + + )   { 
 	 
 	 	 / /   g e t   i t e m   i t e m   i n c l u d i n g   d u e   d a t e   a n d   n o t e s 
 	 	 v a r   i t e m   =   l i s t [ i ] . n a m e ; 
 	 	 i f   ( l i s t [ i ] . d u e D a t e )   i t e m   + =   "   [ D u e :   "   +   l i s t [ i ] . d u e D a t e   +   " ] " ; 
 	 	 i f   ( l i s t [ i ] . b o d y )   i t e m   + =   "   [ N o t e :   "   +   l i s t [ i ] . b o d y   +   " ] " ; 
 	 	 
 	 	 / /   n o n - c o m p l e t e d   i t e m s 
 	 	 i f   ( ! l i s t [ i ] . c o m p l e t e d )   { 
         	 	 t e x t   + =   "&   "   +   i t e m   +   " \ n " ; 
 	 	 	 n + + ; 
 	 	 	 
 	 	 / /   c o m p l e t e d   i t e m s 
 	 	 }   e l s e   { 
 	 	 	 / / t e x t   + =   "&   "   +   i t e m   +   " \ n " ; 
     	 	 	 / / n + + ; 
 	 	 } 
 	 } 
 	 
 	 / /   p a s s   t o   c l i p b o a r d 
 	 a p p . s e t T h e C l i p b o a r d T o ( t e x t ) ; 
 
 	 / /   s h o w   m e s s a g e 
 	 a p p . d i s p l a y A l e r t ( " R e m i n d e r s   C o p i e d " ,   {   m e s s a g e :   n + "   c o p i e d   t o   t h e   c l i p b o a r d . "   } ) ; 
 }                              &jscr  ��ޭ