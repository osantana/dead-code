FasdUAS 1.101.10   ��   ��    k             l     ��  ��    S M This script will tell iSync to synchronize.  if there's more then one device     � 	 	 �   T h i s   s c r i p t   w i l l   t e l l   i S y n c   t o   s y n c h r o n i z e .     i f   t h e r e ' s   m o r e   t h e n   o n e   d e v i c e   
  
 l     ��  ��    . ( attached, I don't know what that means.     �   P   a t t a c h e d ,   I   d o n ' t   k n o w   w h a t   t h a t   m e a n s .      l     ��  ��    M G hints from http://growl.info/documentation/applescript-support.php and     �   �   h i n t s   f r o m   h t t p : / / g r o w l . i n f o / d o c u m e n t a t i o n / a p p l e s c r i p t - s u p p o r t . p h p   a n d      l     ��  ��    E ? http://www.macosxhints.com/article.php?story=20031201172150673     �   ~   h t t p : / / w w w . m a c o s x h i n t s . c o m / a r t i c l e . p h p ? s t o r y = 2 0 0 3 1 2 0 1 1 7 2 1 5 0 6 7 3      l     ��������  ��  ��        l    . ����  O     .    k    -      ! " ! r     # $ # ?     % & % l    '���� ' I   �� (��
�� .corecnte****       **** ( l 	   )���� ) l    *���� * 6    + , + 2    ��
�� 
prcs , =    - . - 1   	 ��
�� 
pnam . m     / / � 0 0  G r o w l H e l p e r A p p��  ��  ��  ��  ��  ��  ��   & m    ����   $ o      ����  0 growlisrunning growlIsRunning "  1 2 1 l   ��������  ��  ��   2  3�� 3 r    - 4 5 4 ?    + 6 7 6 l   ) 8���� 8 I   )�� 9��
�� .corecnte****       **** 9 l 	  % :���� : l   % ;���� ; 6   % < = < 2    ��
�� 
prcs = =   $ > ? > 1     ��
�� 
pnam ? m   ! # @ @ � A A 
 i S y n c��  ��  ��  ��  ��  ��  ��   7 m   ) *����   5 o      ����  0 isyncisrunning iSyncIsRunning��    m      B B�                                                                                  sevs  alis    �  Macintosh HD               ��x�H+     jSystem Events.app                                               5�Ǚk        ����  	                CoreServices    �٢�      Ǚ�,       j   &   %  :Macintosh HD:System:Library:CoreServices:System Events.app  $  S y s t e m   E v e n t s . a p p    M a c i n t o s h   H D  -System/Library/CoreServices/System Events.app   / ��  ��  ��     C D C l     ��������  ��  ��   D  E F E l  / _ G���� G Z   / _ H I���� H o   / 0����  0 growlisrunning growlIsRunning I O   3 [ J K J k   7 Z L L  M N M l  7 7��������  ��  ��   N  O P O l  7 7�� Q R��   Q 1 + Make a list of all the notification types     R � S S V   M a k e   a   l i s t   o f   a l l   t h e   n o t i f i c a t i o n   t y p e s   P  T U T l  7 7�� V W��   V ' ! that this script will ever send:    W � X X B   t h a t   t h i s   s c r i p t   w i l l   e v e r   s e n d : U  Y Z Y r   7 < [ \ [ J   7 : ] ]  ^�� ^ m   7 8 _ _ � ` ` & R e s u l t   N o t i f i c a t i o n��   \ l      a���� a o      ���� ,0 allnotificationslist allNotificationsList��  ��   Z  b c b l  = =��������  ��  ��   c  d e d l  = =�� f g��   f ( " Make a list of the notifications     g � h h D   M a k e   a   l i s t   o f   t h e   n o t i f i c a t i o n s   e  i j i l  = =�� k l��   k - ' that will be enabled by default.          l � m m N   t h a t   w i l l   b e   e n a b l e d   b y   d e f a u l t .             j  n o n l  = =�� p q��   p 9 3 Those not enabled by default can be enabled later     q � r r f   T h o s e   n o t   e n a b l e d   b y   d e f a u l t   c a n   b e   e n a b l e d   l a t e r   o  s t s l  = =�� u v��   u 7 1 in the 'Applications' tab of the growl prefpane.    v � w w b   i n   t h e   ' A p p l i c a t i o n s '   t a b   o f   t h e   g r o w l   p r e f p a n e . t  x y x r   = B z { z J   = @ | |  }�� } m   = > ~ ~ �   & R e s u l t   N o t i f i c a t i o n��   { l      ����� � o      ���� 40 enablednotificationslist enabledNotificationsList��  ��   y  � � � l  C C��������  ��  ��   �  ��� � I  C Z���� �
�� .registernull��� ��� null��   � �� � �
�� 
appl � l 	 E F ����� � m   E F � � � � �  i S y n c S c r i p t��  ��   � �� � �
�� 
anot � l 
 I J ����� � o   I J���� ,0 allnotificationslist allNotificationsList��  ��   � �� � �
�� 
dnot � l 
 M N ����� � o   M N���� 40 enablednotificationslist enabledNotificationsList��  ��   � �� ���
�� 
iapp � m   Q T � � � � � $ A p p l e S c r i p t   E d i t o r��  ��   K m   3 4 � �2                                                                                  GRRR  alis    �  Macintosh HD               ��x�H+   AGrowlHelperApp.app                                              A$�\�        ����  	                	Resources     �٢�      �]4     A A A 
�   �  YMacintosh HD:Library:PreferencePanes:Growl.prefPane:Contents:Resources:GrowlHelperApp.app   &  G r o w l H e l p e r A p p . a p p    M a c i n t o s h   H D  LLibrary/PreferencePanes/Growl.prefPane/Contents/Resources/GrowlHelperApp.app  / ��  ��  ��  ��  ��   F  � � � l     ��������  ��  ��   �  � � � l  ` � ����� � O   ` � � � � k   f � � �  � � � l  f f�� � ���   �   21600 seconds == 6hs    � � � � *   2 1 6 0 0   s e c o n d s   = =   6 h s �  ��� � Z   f � � ����� � A  f u � � � 1   f k��
�� 
lsnc � l  k t ����� � \   k t � � � l  k p ����� � I  k p������
�� .misccurdldt    ��� null��  ��  ��  ��   � m   p s����T`��  ��   � k   x � � �  � � � I  x }������
�� .miscactvnull��� ��� null��  ��   �  � � � I  ~ �������
�� .blrnSYNCbool       obj ��  ��   �  � � � l  � ��� � ���   � 2 , wait until sync status != 1 (synchronizing)    � � � � X   w a i t   u n t i l   s y n c   s t a t u s   ! =   1   ( s y n c h r o n i z i n g ) �  � � � V   � � � � � I  � ��� ���
�� .sysodelanull��� ��� nmbr � m   � ����� ��   � l  � � ����� � =  � � � � � 1   � ���
�� 
syng � m   � ���
�� boovtrue��  ��   �  � � � l  � ���������  ��  ��   �  � � � r   � � � � � 1   � ���
�� 
stsy � o      ���� 0 
syncstatus 
syncStatus �  ��� � r   � � � � � 1   � ���
�� 
lsnc � o      ���� 0 lastsync lastSync��  ��  ��  ��   � m   ` c � ��                                                                                  iSnc  alis    H  Macintosh HD               ��x�H+     q	iSync.app                                                        �����V        ����  	                Applications    �٢�      �� �       q  #Macintosh HD:Applications:iSync.app    	 i S y n c . a p p    M a c i n t o s h   H D  Applications/iSync.app  / ��  ��  ��   �  � � � l     ��������  ��  ��   �  � � � l  � � ���~ � r   � � � � � m   � � � � � � �   � o      �}�}  0 syncstatustext syncStatusText�  �~   �  � � � l     �|�{�z�|  �{  �z   �  � � � l     �y � ��y   � 4 . syncStatus = 2 -> successfully completed sync    � � � � \   s y n c S t a t u s   =   2   - >   s u c c e s s f u l l y   c o m p l e t e d   s y n c �  � � � l  �3 ��x�w � Z   �3 � ��v � � =   � � � � � o   � ��u�u 0 
syncstatus 
syncStatus � m   � ��t�t  � r   � � � � � m   � � � � � � � & S u c c e s s f u l l y   S y n c e d � o      �s�s  0 syncstatustext syncStatusText�v   � k   �3 � �  � � � Z   �1 � � ��r � =   � � � � � o   � ��q�q 0 
syncstatus 
syncStatus � m   � ��p�p  � r   � � � � � m   � � � � � � � . C o m p l e t e d   w i t h   W a r n i n g s � o      �o�o  0 syncstatustext syncStatusText �  � � � =   � � � � � o   � ��n�n 0 
syncstatus 
syncStatus � m   � ��m�m  �  � � � r   � � � � � m   � � � � � � � * C o m p l e t e d   w i t h   E r r o r s � o      �l�l  0 syncstatustext syncStatusText �  � � � =   � � � � � o   � ��k�k 0 
syncstatus 
syncStatus � m   � ��j�j  �  � � � r   � � � � m   �   � & L a s t   S y n c   C a n c e l l e d � o      �i�i  0 syncstatustext syncStatusText �  =   o  �h�h 0 
syncstatus 
syncStatus m  �g�g   r  	 m  

 � 8 L a s t   S y n c   F a i l e d   t o   C o m p l e t e	 o      �f�f  0 syncstatustext syncStatusText  =  # o  �e�e 0 
syncstatus 
syncStatus m  "�d�d  �c r  &- m  &) �  N e v e r   S y n c e d o      �b�b  0 syncstatustext syncStatusText�c  �r   � �a l 22�`�_�^�`  �_  �^  �a  �x  �w   �  l     �]�\�[�]  �\  �[    l 4U�Z�Y Z  4U�X�W F  4B =  49  o  47�V�V 0 
syncstatus 
syncStatus  m  78�U�U  H  <>!! o  <=�T�T  0 isyncisrunning iSyncIsRunning O EQ"#" I KP�S�R�Q
�S .aevtquitnull��� ��� null�R  �Q  # m  EH$$�                                                                                  iSnc  alis    H  Macintosh HD               ��x�H+     q	iSync.app                                                        �����V        ����  	                Applications    �٢�      �� �       q  #Macintosh HD:Applications:iSync.app    	 i S y n c . a p p    M a c i n t o s h   H D  Applications/iSync.app  / ��  �X  �W  �Z  �Y   %&% l     �P�O�N�P  �O  �N  & '(' l Vq)�M�L) r  Vq*+* b  Vm,-, b  Vi./. b  Ve010 b  Va232 b  V]454 m  VY66 �77  S t a t u s :  5 o  Y\�K�K  0 syncstatustext syncStatusText3 l 	]`8�J�I8 m  ]`99 �::    (�J  �I  1 o  ad�H�H 0 
syncstatus 
syncStatus/ m  eh;; �<<  ) .     S y n c e d   o n  - o  il�G�G 0 lastsync lastSync+ o      �F�F 0 displaytext displayText�M  �L  ( =>= l     �E�D�C�E  �D  �C  > ?@? l r�A�B�AA Z  r�BC�@DB o  rs�?�?  0 growlisrunning growlIsRunningC O  v�EFE I z��>�=G
�> .notifygrnull��� ��� null�=  G �<HI
�< 
nameH m  ~�JJ �KK & R e s u l t   N o t i f i c a t i o nI �;LM
�; 
titlL l 	��N�:�9N m  ��OO �PP  i S y n c S c r i p t�:  �9  M �8QR
�8 
descQ o  ���7�7 0 displaytext displayTextR �6ST
�6 
applS l 	��U�5�4U m  ��VV �WW  i S y n c S c r i p t�5  �4  T �3X�2
�3 
iappX m  ��YY �ZZ 
 i S y n c�2  F m  vw[[2                                                                                  GRRR  alis    �  Macintosh HD               ��x�H+   AGrowlHelperApp.app                                              A$�\�        ����  	                	Resources     �٢�      �]4     A A A 
�   �  YMacintosh HD:Library:PreferencePanes:Growl.prefPane:Contents:Resources:GrowlHelperApp.app   &  G r o w l H e l p e r A p p . a p p    M a c i n t o s h   H D  LLibrary/PreferencePanes/Growl.prefPane/Contents/Resources/GrowlHelperApp.app  / ��  �@  D I ���1\�0
�1 .sysodlogaskr        TEXT\ b  ��]^] m  ��__ �``  s y n c S t a t u s :  ^ o  ���/�/ 0 
syncstatus 
syncStatus�0  �B  �A  @ aba l     �.�-�,�.  �-  �,  b c�+c l ��d�*�)d L  ��ee o  ���(�( 0 
syncstatus 
syncStatus�*  �)  �+       �'fg�'  f �&
�& .aevtoappnull  �   � ****g �%h�$�#ij�"
�% .aevtoappnull  �   � ****h k    �kk  ll  Emm  �nn  �oo  �pp qq 'rr ?ss c�!�!  �$  �#  i  j > B� t� /�� @� � _� ~�� ���� ��� �����������
 ��	 � �� �� �
���69;��J� O��VY����_��
�  
prcst  
� 
pnam
� .corecnte****       ****�  0 growlisrunning growlIsRunning�  0 isyncisrunning iSyncIsRunning� ,0 allnotificationslist allNotificationsList� 40 enablednotificationslist enabledNotificationsList
� 
appl
� 
anot
� 
dnot
� 
iapp� 
� .registernull��� ��� null
� 
lsnc
� .misccurdldt    ��� null�T`
� .miscactvnull��� ��� null
� .blrnSYNCbool       obj 
� 
syng
� .sysodelanull��� ��� nmbr
� 
stsy� 0 
syncstatus 
syncStatus�
 0 lastsync lastSync�	  0 syncstatustext syncStatusText� � � � 
� 
bool
� .aevtquitnull��� ��� null� 0 displaytext displayText
� 
name
�  
titl
�� 
desc�� 

�� .notifygrnull��� ��� null
�� .sysodlogaskr        TEXT�"�� +*�-�[�,\Z�81j jE�O*�-�[�,\Z�81j jE�UO� -� %�kvE�O�kvE�O*��a �a �a a a  UY hOa  N*a ,*j a  ;*j O*j O h*a ,e kj [OY��O*a ,E` O*a ,E`  Y hUOa !E` "O_ l  a #E` "Y g_ m  a $E` "Y S_ a %  a &E` "Y ?_ a '  a (E` "Y +_ a )  a *E` "Y _ a +  a ,E` "Y hOPO_ l 	 �a -& a  *j .UY hOa /_ "%a 0%_ %a 1%_  %E` 2O� -� %*a 3a 4a 5a 6a 7_ 2�a 8a a 9a : ;UY a <_ %j =O_  ascr  ��ޭ