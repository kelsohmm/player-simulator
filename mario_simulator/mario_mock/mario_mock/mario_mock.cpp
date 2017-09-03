// mario_mock.cpp : Defines the exported functions for the DLL application.
//

#include "stdafx.h"

#define DLLEXPORT  __declspec(dllexport)

extern "C"
{
	typedef struct {
		bool* activeInputs;
		int length;
	} Inputs;

	typedef struct {
		bool* gamestate;
		int length;
	} Gamestate;

	Gamestate createMockGamestate()
	{
		const int outputLength = 8;

		return Gamestate{
			new bool[outputLength]{ 0, 1, 0, 1, 0, 1, 0, 1 },
			outputLength
		};

	}

	Gamestate createMockGamestate();

	DLLEXPORT Gamestate simulateTour(const Inputs& inputs)
	{
		return createMockGamestate();
	}

	DLLEXPORT Gamestate initializeGamestate()
	{
		return createMockGamestate();
	}

}


