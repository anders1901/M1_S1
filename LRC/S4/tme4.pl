/*Exercice 1 :*/
subs(chat, felin).
subs(lion, felin).
subs(chien, canide).
subs(canide,chien).

subs(souris, mammifere).
subs(felin, mammifere).
subs(canide, mammifere).

subs(mammifere, animal).
subs(canari, animal).
subs(animal, etreVivant).
subs(and(animal, plante), nothing).

subs(and(animal, some(aMaitre)), pet).
subs(pet, some(aMaitre)).
subs(some(aMaitre), all(aMaitre, humain)).
subs(chihuahua,and(chien,pet)).

equiv(carnivoreExc, all(mange, animal)).
equiv(herbivoreExc, all(mange, plante)).

subs(lion, carnivoreExc).
subs(carnivoreExc, predateur).
subs(animal, some(mange)).
subs(and(all(mange, nothing), some(mange)), nothing).

inst(felix, chat).
instR(felix, aMaitre, pierre).
inst(pierre, humain).

inst(princesse, chihuahua).
instR(princesse, aMaitre, marie).
inst(marie, humain).

inst(jerry, souris).
inst(titi, canari).

instR(felix, mange, and(jerry,titi)).

%subs(carnivoreExc,animal).
%subs(herbivoreExc,animal).


/*Exercice 2 :*/
%Question 1:
subsS1(C, C).
subsS1(C, D):- subs(C,D), C\==D.
subsS1(C, D):- subs(C, E), subsS1(E,D).

%Question 3:
/*La requete ne termine pas*/

%Question 4:
subsS(C, D) :- subsS(C, D, [C]).
subsS(C, C, _).
subsS(C, D, _) :- subs(C, D), C\==D.
subsS(C, D, L) :- subs(C, E), not(member(E, L)), subsS(E, D, [E|L]), E\==D.

%Question 7:
/*
subsS(chat, X). :
X devrait prendre comme valeur chat, félin, mammifère, animal, etreVivant, some(mange), c'est bien le cas.

subsS(X, mammifere). :
X devrait prendre comme valeur mammifere, souris, félin, canidé, lion, chat, chien, c’est bien le cas malgré le fait que lion apparait deux fois :
	il apparait dans deux règles de notre base de connaissance qui participent à la résolution de cette requête.
*/

%Question 8:
%equiv(C, D):- and(subs(C, D), subs(D, C)).
subs(C, D) :- equiv(C, D).
subs(D, C) :- equiv(C, D).

%Question 10:
/*
On a plutôt intérêt à dériver de subs, car on réalise plus tôt des déductions sur subs, et ainsi les subsS résultant des subs sont plus nombreux.
*/


/*Exercice 3 :*/
subsS(C,and(D1,D2),L):-D1\=D2,subsS(C,D1,L),subsS(C,D2,L).
subsS(C,D,L):-subs(and(D1,D2),D),E=and(D1,D2),not(member(E,L)), subsS(C,E,[E|L]),E\==C.
subsS(and(C,C),D,L):-nonvar(C),subsS(C,D,[C|L]).
subsS(and(C1,C2),D,L):-C1\=C2,subsS(C1,D,[C1|L]).
subsS(and(C1,C2),D,L):-C1\=C2,subsS(C2,D,[C2|L]).
subsS(and(C1,C2),D,L):-subs(C1,E1),E=and(E1,C2),not(member(E,L)),subsS(E,D,[E|L]),E\==D.
subsS(and(C1,C2),D,L):-Cinv=and(C2,C1),not(member(Cinv,L)),subsS(Cinv,D,[Cinv|L]).

%Question 2:
/*
R1) Cas où on subsume a une intersection: on regarde si les 2 subsomptions séparées sont vraies.
    ex : subsS(chihuahua,and(mammifere,some(aMaitre))). ne fonctionne pas sans celle ci.
R2) Cas qui permet de descendre dans les subsomptions avec intersections si elles existent
R3) si C est une variable définie, il suffit juste de faire le subsS d'origine.
    ex : subsS(and(X,X),pet). ne fonctionne pas sans celle ci
R4) On vérifie si le premier membre de l'intersection subsume
R5) Ou bien si le second membre de l'intersection subsume
R6) Permet de remonter les subsomptions
R7) inverse l'intersection pour faire le parcours de la ligne precedente sur le second membre de la subsomptions
*/


/*Exercice 4 :*/
%Question 1 :
subsS(C, all(R, D), L):- subs(E1, D), E = all(R, E1), not(member(E, L)), subsS(C, E, [E|L]).
subsS(all(R, C), D, L):- subs(C, E1), E = all(R, E1), not(member(E, L)), subsS(E, D, [E|L]).

%Question 3:
subs(and(carnivoreExc,herbivoreExc),nothing).

%Question 4:
subsS(all(R, inst(_, C)), all(R, C), _).
