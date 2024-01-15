#include <stdlib.h>
#include<cmath>

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

bool wireframe = false;
// function called everytime the windows is refreshed
void display () 
{

    // clear window 
    glClear(GL_COLOR_BUFFER_BIT);

    // draw scene
    if (wireframe){
        glutSolidTeapot(.5);
    }
    else {
        glutWireTeapot(.5); 
    }

    // flush drawing routines to the window 
    glFlush();

}

// Function called everytime a key is pressed
void key( unsigned char key, int, int)
{
    switch ( key )
    {
    	// the 'esc' key
        case 27:
        // the 'q' key
        case 'q':
            exit( EXIT_SUCCESS );
            break;
        case 'w' :
            wireframe = !wireframe;
    }
    glutPostRedisplay( );
}

// Function called every time the main window is resized
void reshape ( int width, int height )
{
    int width_new = width;
    int height_new = height;
    int or_x = 0;
    int or_y =0;
    if (width > height)
    {
        width_new = height;
        or_x = (width - height)/2;
    }
    else
    {
        or_y = (height - width)/2;
        height_new = width;
    }

    // define the viewport transformation;
    glViewport(or_x,or_y,width_new,height_new);
}


// Main routine
int main ( int argc, char * argv[] ) 
{

    // initialize GLUT, using any commandline parameters passed to the 
    //   program 
    glutInit( &argc, argv );

    // setup the size, position, and display mode for new windows 
    glutInitWindowSize( 500, 500 );
    glutInitWindowPosition( 0, 0 );
    glutInitDisplayMode( GLUT_RGB );

    // create and set up a window 
    glutCreateWindow("Hello, teapot!");
    
    // Set up the callback functions:
    // for display
    glutDisplayFunc( display );
    // for the keyboard
    glutKeyboardFunc( key );
    // for reshaping
    glutReshapeFunc( reshape );


    // define the projection transformation
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluPerspective(60,1,1.0,10);
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    gluLookAt(0.0,0.0,-2.0,0.0,0.0,0.0,1.0,1.0,0.0);

    // tell GLUT to wait for events 
    glutMainLoop();
}
