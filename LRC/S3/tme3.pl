/*Exercice 2 :*/
%Question 1 :
concatene([],L,L).
concatene([A|X],Y,[A|Z]):-concatene(X,Y,Z).

%Question 2 :
inverse([], []):-!.
inverse(X, [YT|YQ]):-concatene(Z,[YT],X),inverse(Z,YQ).

%Question 3 :
supprime([],_,[]).
supprime([A|X],Y,[A|Z]):-A\==Y, supprime(X,Y,Z).
supprime([A|X],A,Z):-supprime(X,A,Z).

%Question 4 :
filtre(X,[],X).
filtre(L1,[L2T|L2Q],L3):-supprime(L1,L2T,Z),filtre(Z,L2Q,L3).


/*Exercice 3 :*/
%Question 1 :
palindrome(X):-inverse(X,Y), Y==X.

%Question2 :
palindrome2([_]).
palindrome2([]).
palindrome2([XT|XQ]):-concatene(L,[XT],XQ), palindrome2(L).
