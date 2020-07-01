/*Exercice 4*/
pere(carlos,andersson).
pere(carlos,matthiew).
pere(guilermo,carlos).
pere(guilermo,dario).
pere(guilermo,santiago).
pere(guilermo,fernanda).
pere(guillermo,alexandra).
pere(guillermo,alexis).
pere(guillermo,angel).
pere(guillermo,rosa).
pere(guillermo,rojelio).
pere(guillermo,kleber).
pere(guillermo,rafael).
mere(alexandra,andersson).
mere(alexandra,matthiew).
mere(egma,carlos).
mere(egma,dario).
mere(egma,santiago).
mere(egma,fernanda).
mere(beatriz,alexandra).
mere(beatriz,alexis).
mere(beatriz,angel).
mere(beatriz,rosa).
mere(beatriz,rojelio).
mere(beatriz,kleber).
mere(beatriz,rafael).
parent(X,Y) :- pere(X,Y).
parent(X,Y) :- mere(X,Y).
parents(X,Y,Z) :- pere(X,Z), mere(Y,Z).
grandPere(X,Y) :- pere(X,Z), parent(Z,Y).
grandMere(X,Y) :- mere(X,Z), parent(Z,Y).
/*frereOuSoeur(X,Y) :- parent(Z,X), parent(Z,Y). au sens large du terme */
frereOuSoeur(X,Y) :- parents(P,M,X), parents(P,M,Y), X\=Y.
ancetre(X,Y) :- parent(X,Y).
ancetre(X,Y) :- grandPere(X,Y).
ancetre(X,Y) :- grandMere(X,Y).


/*Exercice 5*/

%"et" logique
et(0,1,0).
et(1,0,0).
et(0,0,0).
et(1,1,1).

%"ou" logique
ou(0,0,0).
ou(0,1,1).
ou(1,0,1).
ou(1,1,1).

%"non" logique
non(0,1).
non(1,0).

%circuit
xor(X,Y,Z):-ou(X,Y,T), X\==1,Y\==1.
xor(1,1,0).
nand(X,Y,Z):-et(X,Y,T),non(T,Z).
circuit(X,Y,Z):-nand(X,Y,U), non(X,T), xor(U,T,W), non(W,Z).
