#include <cstdlib>

// for mac osx
#ifdef __APPLE__
#include <OpenGL/gl.h>
#include <OpenGL/glu.h>
#include <GLUT/glut.h>
#else
// only for windows
#ifdef _WIN32
#include <windows.h>
#endif
// for windows and linux
#include <GL/gl.h>
#include <GL/glu.h>
#include <GL/freeglut.h>
#endif


#include <iostream>
using namespace std;

GLfloat cameraX = 0.0f;
GLfloat cameraY = 0.0f;
GLfloat cameraZ = 5.0f;
GLfloat angleX = 0.0f;
GLfloat angleY = 0.0f;
const GLfloat SPEED = 0.1f;
const GLfloat ANG_SPEED = 0.5f;

void display ()
{

    /* clear window */
    glClear(GL_COLOR_BUFFER_BIT);

    // set current matrix as GL_MODELVIEW
    glMatrixMode(GL_MODELVIEW);

    // draw scene

    // add a copy of the curr. matrix to the stack
    glPushMatrix();

        glPushMatrix();
            // translate by -3 on the z
            glTranslatef(0, 0, -3);
            // set drawing color to red
            glColor3f(1.0f, 0.0f, 0.0f);
            // middle red teapot
            glutWireTeapot( 1 );
            // translate by 2 on the y
            glTranslatef(0, 2, 0);
            // set drawing color to blue
            glColor3f(0.0f, 1.0f, 0.0f);
            // rotate 90 deg around x
            glRotatef(90, 1.0f, 0.0f, 0.0f);
            // top green teapot
            glutWireTeapot( 1 );
        // pop the current matrix
        glPopMatrix();

        // translate -2 on y and -1 on z
        glTranslatef(0, -2, -1);
        // set drawing color to blue
        glColor3f(0.0f, 0.0f, 1.0f);
        // bottom blue teapot
        glutWireTeapot( 1 );

    // pop the current matrix
    glPopMatrix();
    

    /* flush drawing routines to the window */
    glFlush();

}

// Function called every time a key is pressed
void key(unsigned char key, int, int)
    {
        switch (key)
        {
            case 'w':
                cameraZ -= SPEED;
                break;
            case 's':
                cameraZ += SPEED;
                break;
            case 'a':
                cameraX -= SPEED;
                break;
            case 'd':
                cameraX += SPEED;
                break;
            case 'z':
                cameraY += SPEED;
                break;
            case 'q':
            case 27:  // Esc key
                exit(EXIT_SUCCESS);
                break;
        }
        glLoadIdentity();
        gluLookAt(cameraX, cameraY, cameraZ, angleX, angleY, 0.0, 0.0, 1.0, 0.0);

        glutPostRedisplay();
    }

void reshape ( int width, int height )
{

    /* define the viewport transformation */
    glViewport(0,0,width,height);

}

void specialFunc(int key, int x, int y) 
{
        switch (key) {
            case GLUT_KEY_LEFT:
                angleY -= ANG_SPEED;
                break;
            case GLUT_KEY_RIGHT:
                angleY += ANG_SPEED;
                break;
            case GLUT_KEY_UP:
                angleX -= ANG_SPEED;
                break;
            case GLUT_KEY_DOWN:
                angleX += ANG_SPEED;
                break;
    }
    glLoadIdentity();
    gluLookAt(cameraX, cameraY, cameraZ, angleX, angleY, 0.0, 0.0, 1.0, 0.0);
    glutPostRedisplay();
}

int main ( int argc, char * argv[] )
{

    /* initialize GLUT, using any commandline parameters passed to the 
       program */
    glutInit(&argc,argv);

    /* setup the size, position, and display mode for new windows */
    glutInitWindowSize(500,500);
    glutInitWindowPosition(0,0);
    glutInitDisplayMode(GLUT_RGB);

    /* create and set up a window */
    glutCreateWindow("hello, teapot!");
    // Set up the callback functions
    // for display
    glutDisplayFunc( display );
    // for the keyboard
    glutKeyboardFunc( key );
    // for reshaping
    glutReshapeFunc( reshape );

    /* define the projection transformation */
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluPerspective(60,1,1,10);
    
    /* define the viewing transformation */
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    gluLookAt(cameraX, cameraY, cameraZ,0.0,0.0,-1.0,0.0,1.0,0.0);

    glutKeyboardFunc( key );
    glutSpecialFunc(specialFunc);
    /* tell GLUT to wait for events */
    glutMainLoop();
}