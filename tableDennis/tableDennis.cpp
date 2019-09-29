/*
 * tableDennis.cpp
 *
 *  Created on: Aug 3, 2019
 *      Author: dennis.fisher_snhu
 */

#include <windows.h>
#include <iostream>
#include <GL/freeglut.h>
#include <GL/GL.h>
#include <GL/glut.h>
#include <GL/glew.h>

//GLM Math Header Inclusions */
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/type_ptr.hpp>

#include "SOIL2/SOIL2.h"

using namespace std;

/*Shader program Macro*/
#ifndef GLSL
#define GLSL(Version, Source) "#version " #Version "\n" #Source
#endif

/*Variable declarations for shader, window size initialization, buffer and array objects*/
GLint shaderProgram;
GLuint texture;

void drawScene(void);
void UCreateShader(void);
void UGenerateTexture(void);

void UMouseMove(int x, int y);
void processSpecialKeys(int key, int xx, int yy);
void UGenerateTexture(void);

// Scaling of the object
GLfloat scale_by_y = 2.0f;
GLfloat scale_by_z = 2.0f;
GLfloat scale_by_x = 2.0f;

int view_state = 1; // Orthogonal view = 1, Perspective = 0

GLfloat lastMouseX = 400, lastMouseY = 300; //locks mouse cursor at the center of the screen
GLfloat sumX = 0, sumY = 0;
GLfloat mouseXoffset, mouseYoffset, yaw = 0.0f, pitch = 0.0f; //mouse offset , yaw and pitch variables
GLfloat sensitivity = 0.01f; //used for mouse and camera sensitivity

GLint WindowWidth = 1200, WindowHeight = 960;

// angle of rotation for the camera direction
float angle = 0.0;
// actual vector representing the camera's direction
float lx = 0.0f, lz = 0.0f;
// XZ position of the camera
float x = 0.0f, z = 0.0f;

//camera position
float cam_x = 0.0f;
float cam_y = 0.0f;
float cam_z = -1.0f;

//colors
float red = 1.0f;
float green = 1.0f;
float blue = 1.0f;

/* Vertex Shader Source Code*/
const char * vertexShaderSource = "#version 400 core\n"
// Vertex data from Vertex Attrib Pointer 0
				"layout(location = 0) in vec3 vPosition;"
				// Color data from Vertex Attrib Pointer 1
				"layout(location = 2) in vec2 textureCoordinate;"
				//variable to transfer color data to the fragment shader
				"out vec2 mobileTextureCoordinate;"
				//Global variables for the transform matrices
				"uniform mat4 model;"
				"uniform mat4 view;"
				"uniform mat4 projection;"
				"void main()\n"
				"{\n"
				// transforms vertices to clip coordinates
				"gl_Position =  projection * view * model * vec4(vPosition, 1.0f);"
				// references incoming color data
				"mobileTextureCoordinate  = vec2(textureCoordinate.x,1.0f - textureCoordinate.y);"
				"}\n";

/* Fragment Shader Source Code*/
const char * fragmentShaderSource = "#version 400 core\n"
// Variable to hold incoming color data from vertex shader
				"in vec2 mobileTextureCoordinate;"
				"out vec4 gpuTexture;"
				//"out vec4 gpuColor;"  // Variable to pass color data to the GPU
				"uniform sampler2D uTexture;"
				"void main()\n"
				"{\n"
				"gpuTexture = texture(uTexture, mobileTextureCoordinate);"
				"}\n";


//Initializes 3D rendering
void initRendering() {
	glEnable(GL_DEPTH_TEST);
	glEnable(GL_COLOR_MATERIAL);
	glEnable(GL_LIGHTING); //Enable lighting
	glEnable(GL_LIGHT0); //Enable light #0
	glEnable(GL_LIGHT1); //Enable light #1
	glEnable(GL_NORMALIZE); //Automatically normalize normals
	glShadeModel(GL_SMOOTH); //Enable smooth shading
}

//Called when the window is resized
void handleResize(int w, int h) {
	glMatrixMode(GL_PROJECTION);
	glLoadIdentity();
	WindowWidth = w;
	WindowHeight = h;
	glViewport(0.0f, 0.0f, WindowWidth, WindowHeight);
}

float _angle = -70.0f;

//Draws the 3D scene
void drawScene() {

	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

	//Change between orthogonal view and perspective view
	if (view_state == 1) {
		//Perspective view
		glMatrixMode(GL_PROJECTION);
		glLoadIdentity();
		gluPerspective(45.0, (GLfloat) WindowWidth / (GLfloat) WindowHeight, 0.1f, 100.0f);
		glMatrixMode(GL_MODELVIEW);
		glLoadIdentity();
	} else if (view_state == 0) {
		//Orthogonal view
		glMatrixMode(GL_PROJECTION);
		glLoadIdentity();
		glOrtho(-5.0f, 5.0f, -5.0f, 5.0f, 0.1f, 100.0f);
		glMatrixMode(GL_MODELVIEW);
		glLoadIdentity();
	}

	glTranslatef(0.0f, 0.0f, -14.0f);
	gluLookAt(cam_x, cam_y, cam_z, x, 0.0f, z, x + lx, 1.0f, z + lz);

	//this will allow for zooming in and out
	glScalef(scale_by_x, scale_by_y, scale_by_z);

	//Add ambient light
	GLfloat ambientColor[] = { 0.2f, 0.0f, 0.0f, 1.0f }; //Color (0.2, 0.0, 0.0)
	glLightModelfv(GL_LIGHT_MODEL_AMBIENT, ambientColor);

	//Add positioned light
	GLfloat lightColor0[] = {red, green, blue, 1.0f }; //Color (1.0, 1.0, 1.0)
	GLfloat lightPos0[] = { 0.0f, -8.0f, 8.0f, 1.0f }; //Positioned at (4, 0, 8)
	glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor0);
	glLightfv(GL_LIGHT0, GL_POSITION, lightPos0);

	//Add directed light
	GLfloat lightColor1[] =  {red, green, blue, 1.0f }; //Color (1.0, 1.0, 1.0)
	//Coming from the direction (-1, 0.5, 0.5)
	GLfloat lightPos1[] = { -1.0f, 0.5f, 0.5f, 0.0f };
	glLightfv(GL_LIGHT1, GL_DIFFUSE, lightColor1);
	glLightfv(GL_LIGHT1, GL_POSITION, lightPos1);

	glRotatef(10, 1.0f, 0.0f, 0.0f);
	glRotatef(-10, 0.0f, 0.0f, 1.0f);
	glRotatef(_angle, 0.0f, 1.0f, 0.0f);

	glColor3f(1.0f, 0.9f, 1.0f);
	glBegin(GL_QUADS);

	//Front
	glNormal3f(0.0f, 0.0f, 1.0f);
	glVertex3f(-2.0f, -0.2f, 2.0f);
	glVertex3f(2.0f, -0.2f, 2.0f);
	glVertex3f(2.0f, 0.2f, 2.0f);
	glVertex3f(-2.0f, 0.2f, 2.0f);

	//Right
	glNormal3f(1.0f, 0.0f, 0.0f);
	glVertex3f(2.0f, -0.2f, -2.0f);
	glVertex3f(2.0f, 0.2f, -2.0f);
	glVertex3f(2.0f, 0.2f, 2.0f);
	glVertex3f(2.0f, -0.2f, 2.0f);

	//Back
	glNormal3f(0.0f, 0.0f, -1.0f);
	glVertex3f(-2.0f, -0.2f, -2.0f);
	glVertex3f(-2.0f, 0.2f, -2.0f);
	glVertex3f(2.0f, 0.2f, -2.0f);
	glVertex3f(2.0f, -0.2f, -2.0f);

	//Left
	glNormal3f(-1.0f, 0.0f, 0.0f);
	glVertex3f(-2.0f, -0.2f, -2.0f);
	glVertex3f(-2.0f, -0.2f, 2.0f);
	glVertex3f(-2.0f, 0.2f, 2.0f);
	glVertex3f(-2.0f, 0.2f, -2.0f);

	//top
	glNormal3f(0.0f, 1.0f, 0.0f);
	glVertex3f(2.0f, 0.2f, 2.0f);
	glVertex3f(-2.0f, 0.2f, 2.0f);
	glVertex3f(-2.0f, 0.2f, -2.0f);
	glVertex3f(2.0f, 0.2f, -2.0f);

	//bottom
	glNormal3f(0.0f, -1.0f, 0.0f);
	glVertex3f(2.0f, -0.2f, 2.0f);
	glVertex3f(-2.0f, -0.2f, 2.0f);
	glVertex3f(-2.0f, -0.2f, -2.0f);
	glVertex3f(2.0f, -0.2f, -2.0f);

	//table front leg
	//front
	glNormal3f(0.0f, 0.0f, 1.0f);
	glVertex3f(1.8f, -0.2f, 1.6f);
	glVertex3f(1.4f, -0.2f, 1.6f);
	glVertex3f(1.4f, -3.0f, 1.6f);
	glVertex3f(1.8f, -3.0f, 1.6f);

	//back
	glNormal3f(0.0f, 0.0f, -1.0f);
	glVertex3f(1.8f, -0.2f, 1.2f);
	glVertex3f(1.4f, -0.2f, 1.2f);
	glVertex3f(1.4f, -3.0f, 1.2f);
	glVertex3f(1.8f, -3.0f, 1.2f);

	//right
	glNormal3f(1.0f, 0.0f, 0.0f);
	glVertex3f(1.8f, -0.2f, 1.6f);
	glVertex3f(1.8f, -0.2f, 1.2f);
	glVertex3f(1.8f, -3.0f, 1.2f);
	glVertex3f(1.8f, -3.0f, 1.6f);

	//left
	glNormal3f(-1.0f, 0.0f, 0.0f);
	glVertex3f(1.4f, -0.2f, 1.6f);
	glVertex3f(1.4f, -0.2f, 1.2f);
	glVertex3f(1.4f, -3.0f, 1.2f);
	glVertex3f(1.4f, -3.0f, 1.6f);

	//back leg back
	//front
	glNormal3f(0.0f, 0.0f, -1.0f);
	glVertex3f(1.8f, -0.2f, -1.2f);
	glVertex3f(1.4f, -0.2f, -1.2f);
	glVertex3f(1.4f, -3.0f, -1.2f);
	glVertex3f(1.8f, -3.0f, -1.2f);

	//back
	glNormal3f(0.0f, 0.0f, -1.0f);
	glVertex3f(1.8f, -0.2f, -1.6f);
	glVertex3f(1.4f, -0.2f, -1.6f);
	glVertex3f(1.4f, -3.0f, -1.6f);
	glVertex3f(1.8f, -3.0f, -1.6f);

	//right
	glNormal3f(1.0f, 0.0f, 0.0f);
	glVertex3f(1.8f, -0.2f, -1.6f);
	glVertex3f(1.8f, -0.2f, -1.2f);
	glVertex3f(1.8f, -3.0f, -1.2f);
	glVertex3f(1.8f, -3.0f, -1.6f);

	//left
	glNormal3f(1.0f, 0.0f, 0.0f);
	glVertex3f(1.4f, -0.2f, -1.6f);
	glVertex3f(1.4f, -0.2f, -1.2f);
	glVertex3f(1.4f, -3.0f, -1.2f);
	glVertex3f(1.4f, -3.0f, -1.6f);

	//leg left front
	glNormal3f(0.0f, 0.0f, 1.0f);
	glVertex3f(-1.8f, -0.2f, 1.6f);
	glVertex3f(-1.4f, -0.2f, 1.6f);
	glVertex3f(-1.4f, -3.0f, 1.6f);
	glVertex3f(-1.8f, -3.0f, 1.6f);

	//back
	glNormal3f(0.0f, 0.0f, -1.0f);
	glVertex3f(-1.8f, -0.2f, 1.2f);
	glVertex3f(-1.4f, -0.2f, 1.2f);
	glVertex3f(-1.4f, -3.0f, 1.2f);
	glVertex3f(-1.8f, -3.0f, 1.2f);

	//right
	glNormal3f(1.0f, 0.0f, 0.0f);
	glVertex3f(-1.8f, -0.2f, 1.6f);
	glVertex3f(-1.8f, -0.2f, 1.2f);
	glVertex3f(-1.8f, -3.0f, 1.2f);
	glVertex3f(-1.8f, -3.0f, 1.6f);

	//left
	glNormal3f(-1.0f, 0.0f, 0.0f);
	glVertex3f(-1.4f, -0.2f, 1.6f);
	glVertex3f(-1.4f, -0.2f, 1.2f);
	glVertex3f(-1.4f, -3.0f, 1.2f);
	glVertex3f(-1.4f, -3.0f, 1.6f);


	//left leg back front
	//front
	glNormal3f(0.0f, 0.0f, -1.0f);
	glVertex3f(-1.8f, -0.2f, -1.2f);
	glVertex3f(-1.4f, -0.2f, -1.2f);
	glVertex3f(-1.4f, -3.0f, -1.2f);
	glVertex3f(-1.8f, -3.0f, -1.2f);

	//back
	glNormal3f(0.0f, 0.0f, -1.0f);
	glVertex3f(-1.8f, -0.2f, -1.6f);
	glVertex3f(-1.4f, -0.2f, -1.6f);
	glVertex3f(-1.4f, -3.0f, -1.6f);
	glVertex3f(-1.8f, -3.0f, -1.6f);

	//right
	glNormal3f(1.0f, 0.0f, 0.0f);
	glVertex3f(-1.8f, -0.2f, -1.6f);
	glVertex3f(-1.8f, -0.2f, -1.2f);
	glVertex3f(-1.8f, -3.0f, -1.2f);
	glVertex3f(-1.8f, -3.0f, -1.6f);

	//left
	glNormal3f(-1.0f, 0.0f, 0.0f);
	glVertex3f(-1.4f, -0.2f, -1.6f);
	glVertex3f(-1.4f, -0.2f, -1.2f);
	glVertex3f(-1.4f, -3.0f, -1.2f);
	glVertex3f(-1.4f, -3.0f, -1.6f);

	glBindTexture(GL_TEXTURE_2D, texture);

	glEnd();
	glutSwapBuffers();
}

void update(int value) {
	//_angle += 1.5f;
	if (_angle > 360) {
		_angle -= 360;
	}

	glutPostRedisplay();
	glutTimerFunc(25, update, 0);
}

void UMouseMove(int curr_x, int curr_y) {

	//change camera position
	cam_x = 10.0f * cos(yaw);
	cam_y = 10.0f * sin(pitch);
	cam_z = sin(yaw) * cos(pitch) * 10.0f;

	//gets the direction the mouse was moved
	mouseXoffset = curr_x - lastMouseX;
	mouseYoffset = lastMouseY - curr_y;

	//updates with new mouse coordinates
	lastMouseX = curr_x;
	lastMouseY = curr_y;

	//Applies sensitivity to mouse direction
	mouseXoffset *= sensitivity;
	mouseYoffset *= sensitivity;

	//get the direction of the mouse
	// changes in yaw, then it is moving along X
	if (yaw != yaw + mouseXoffset && pitch == pitch + mouseYoffset) {

		//Increment yaw
		yaw += mouseXoffset;
		//else movement in y
	} else if (pitch != pitch + mouseYoffset && yaw == yaw + mouseXoffset) {

		//Increment y to move vertical
		pitch += mouseYoffset;
	}

	//Maintains a 90 degree pitch for lock
	if (pitch > 89.0f) {

		pitch = 89.0f;
	}

	if (pitch < -89.0f) {
		pitch = -89.0f;
	}

	//update camera position

	cam_x = 5.0f * cos(yaw);
	cam_y = 5.0f * sin(pitch);
	cam_z = sin(yaw) * cos(pitch) * 10.0f;

}

void processSpecialKeys(int key, int xx, int yy) {

	//zooming object
	switch (key) {
		//zoom object out
		case GLUT_KEY_UP:
			scale_by_y += 0.1f;
			scale_by_x += 0.1f;
			scale_by_z += 0.1f;
			break;

		//zoom object in
		case GLUT_KEY_DOWN:
			scale_by_y -= 0.1f;
			scale_by_x -= 0.1f;
			scale_by_z -= 0.1f;
			break;

		//change view state to orthogonal
		case GLUT_KEY_LEFT:
			view_state = 0;
			break;

		//change view state to perspective
		case GLUT_KEY_RIGHT:
			view_state = 1;
			break;

		//more red
		case GLUT_KEY_F1:
			if (red <1.0)
				red += 0.1f;
			break;
		//less red
		case GLUT_KEY_F2:
			if (red > 0.0)
				red -= 0.1f;
			break;
		//more green
		case GLUT_KEY_F3:
			if (green <1.0)
				green += 0.1f;
			break;
		//less green
		case GLUT_KEY_F4:
			if (green > 0.0)
				green -= 0.1f;
			break;
		//more blue
		case GLUT_KEY_F5:
			if (blue <1.0)
				blue += 0.1f;
			break;
		//less blue
		case GLUT_KEY_F6:
			if (blue > 0.0)
				blue -= 0.1f;
			break;
	}
}

int main(int argc, char** argv) {
	//Initialize GLUT
	glutInit(&argc, argv);
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH);
	glutInitWindowSize(1200, 960);

	//Create the window
	glutCreateWindow("Dennis Fisher - Table");
	initRendering();

	//Set handler functions
	glutDisplayFunc(drawScene);

	glutReshapeFunc(handleResize);

	glutPassiveMotionFunc(UMouseMove);

	glutSpecialFunc(processSpecialKeys);
	UCreateShader();
	UGenerateTexture();
	update(0);

	glutMainLoop();
	return 0;
}

/* Create the Shader program*/
void UCreateShader(){
	// Vertex shader
	GLint vertexShader = glCreateShader(GL_VERTEX_SHADER); // Creates the vertex shader
	glShaderSource(vertexShader, 1, &vertexShaderSource, NULL); // Attaches the Vertex shader to the source code
	glCompileShader(vertexShader); // Compiles the Fragment shader

	//Fragment Shader
	GLint fragmentShader = glCreateShader(GL_FRAGMENT_SHADER); // Create the Fragment shader
	glShaderSource(fragmentShader, 1, &fragmentShaderSource, NULL); // Attaches the Fragment shader to source code
	glCompileShader(fragmentShader); // Compiles the Fragment shader

	// Shader program
	shaderProgram = glCreateProgram(); // Creates the Shader program and returns an id
	glAttachShader(shaderProgram, vertexShader); // Attach vertex shader to shader program
	glAttachShader(shaderProgram, fragmentShader);
	; // Attach Fragment shader to the Shader program
	glLinkProgram(shaderProgram); //Link Vertex and Fragment shaders to Shader program

	// Delete the vertex and Fragment shaders once linked
	glDeleteShader(vertexShader);
	glDeleteShader(fragmentShader);

}

void UGenerateTexture() {

	//generating and loading texture
	glGenTextures(1, &texture);
	glBindTexture(GL_TEXTURE_2D, texture);
	int width, height;

	//load image from project folder
	unsigned char* image = SOIL_load_image("snhu.jpg", &width, &height, 0,
			SOIL_LOAD_RGB);

	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB,
			GL_UNSIGNED_BYTE, image);
	glGenerateMipmap(GL_TEXTURE_2D);
	SOIL_free_image_data(image);
	glBindTexture(GL_TEXTURE_2D, 0);

}
