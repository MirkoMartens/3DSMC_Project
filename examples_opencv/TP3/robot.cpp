
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
#define vitesse_angle 5
#define vitesse_pincer 0.1


#include <iostream>
using namespace std;


// Global variables to animate the robotic arm
float angle1 = 0;
float angle2 = 0;
float deltaPincer = 0;

// Global variables to rotate the arm as a whole
float robotAngleX = 0;
float robotAngleY = 0;








/**
 * Function that draws the reference system (three lines along the x, y, z axis)
 */
void drawReferenceSystem()
{
    //**********************************
    // set the line width to 3.0
    //**********************************
    glLineWidth(3.0);
    //**********************************
    // Draw three lines along the x, y, z axis to represent the reference system
    // Use red for the x-axis, green for the y-axis and blue for the z-axis
    //**********************************
    glBegin(GL_LINES);
        glColor3f(1,0,0);
        glVertex3f(0,0,0);
        glVertex3f(1,0,0);

        glColor3f(0,1,0);
        glVertex3f(0,0,0);
        glVertex3f(0,1,0);

        glColor3f(0,0,3);
        glVertex3f(0,0,0);
        glVertex3f(0,0,1);
    glEnd();

    //**********************************
    // reset the drawing color to white
    //**********************************
    glColor3f(1,1,1);
    //**********************************glColor3f(0,1,0);
    // reset the line width to 1.0
    //**********************************
    glLineWidth(1.0);
}


/**
 * Function that draws a single joint of the robotic arm
 */
void drawJoint()
{
    // first draw the reference system
    drawReferenceSystem();

    // Draw the joint as a parallelepiped (a cube scaled on the y-axis)
    //**********************************
    // Bring the cube "up" so that the bottom face is on the xz plane
    //**********************************


    //**********************************
    // draw the scaled cube. Remember that the scaling has to be only
    // on the local reference system, hence we need to get a local copy
    // of the modelview matrix...
    //**********************************
    glPushMatrix();
    glColor3f(1,0,0);
    /*glBegin(GL_QUADS);
        glVertex3f(0,0,1);
        glVertex3f(0,1,1);
        glVertex3f(0,0,0);
        glVertex3f(0,1,0);
    glEnd();
    */
    glScalef(1,2,1);
    glTranslatef(0,0.5,0);
    glutWireCube(1);
    glPopMatrix();
}

/**
 * Function that draws a single joint of the robotic arm
 */
void drawPincer()
{
    // first draw the reference system
    drawReferenceSystem();

    // Draw the joint as a parallelepiped (a cube scaled on the y-axis)
    //**********************************
    // Bring the cube "up" so that the bottom face is on the xz plane
    //**********************************


    //**********************************
    // draw the scaled cube. Remember that the scaling has to be only
    // on the local reference system, hence we need to get a local copy
    // of the modelview matrix...
    //**********************************
    glPushMatrix();
    glColor3f(0,1,0);
     // Draw the vertical rectangles (pincers)
    glPushMatrix();
    glTranslatef(-0.5, 0.5, deltaPincer);
    glScalef(0.2, 1, 0.2);
    glutWireCube(1);
    glPopMatrix();

    glPushMatrix();
    glTranslatef(0.5, 0.5, 2-2*deltaPincer);
    glScalef(0.2, 1, 0.2);
    glutWireCube(1);
    glPopMatrix();

    // Draw the horizontal rectangle (base of the pincers)
    glPushMatrix();
    glTranslatef(0, 0, 0.5);
    glScalef(1, 0.2, 0.2);
    glutWireCube(1);
    glPopMatrix();

    glPopMatrix();
}

/**
 * Function that draws the robot as three parallelepipeds
 */
void drawRobot()
{
    //**********************************
    // we work on a copy of the current MODELVIEW matrix, hence we need to...
    //**********************************
    glPushMatrix();

    // draw the first joint
    drawJoint();

    // Draw the other joints: every joint must be placed on top of the previous one
    // and rotated according to the relevant Angle
    //**********************************
    // the second joint
    //**********************************
    glTranslatef(0, 2, 0);
    glRotatef(angle1, 0.0f, 0.0f, 1.0f);
    drawJoint();
    //**********************************
    // the third joint
    //**********************************
    glTranslatef(0,2,0);
    glRotatef(angle2, 0.0f, 0.0f, 1.0f);
    drawJoint();
    //**********************************
    // the Pincer
    //**********************************
    glTranslatef(0,2,0);
    drawPincer();
    //**********************************
    // "Release" the copy of the current MODELVIEW matrix
    //**********************************
    glPopMatrix();

}


/**
 * Function that handles the display callback (drawing routine)
 */
void display()
{
    // clear the window
    glClear(GL_COLOR_BUFFER_BIT);

    // working with the GL_MODELVIEW Matrix
    glMatrixMode(GL_MODELVIEW);

    //**********************************
    // we work on a copy of the current MODELVIEW matrix, hence we need to...
    //**********************************
    glPushMatrix();


    //**********************************
    // Rotate the robot around the x-axis and y-axis according to the relevant angles
    //**********************************
    glRotatef(robotAngleX,robotAngleY,0.0f,1.0f);

    // draw the robot
    drawRobot();

    //**********************************
    // "Release" the copy of the current MODELVIEW matrix
    //**********************************
    glPopMatrix();

    // flush drawing routines to the window
    glutSwapBuffers();
}


/**
 * Function that handles the special keys callback
 * @param[in] key the key that has been pressed
 * @param[in] x the mouse in window relative x-coordinate when the key was pressed
 * @param[in] y the mouse in window relative y-coordinate when the key was pressed
 */
void arrows(int key, int, int)
{
    //**********************************
    // Manage the update of RobotAngleX and RobotAngleY with the arrow keys
    //**********************************
    switch (key) {
        case GLUT_KEY_UP:
            robotAngleX += vitesse_angle;
            break;
        case GLUT_KEY_DOWN:
            robotAngleX -= vitesse_angle;
            break;
        case GLUT_KEY_LEFT:
            robotAngleY += vitesse_angle;
            break;
        case GLUT_KEY_RIGHT:
            robotAngleY -= vitesse_angle;
            break;
        default:
            break;
    }
    glutPostRedisplay();
}


/**
 * Function that handles the keyboard callback
 * @param key  the key that has been pressed
 * @param[in] x the mouse in window relative x-coordinate when the key was pressed
 * @param[in] y the mouse in window relative y-coordinate when the key was pressed
 */
void keyboard(unsigned char key, int, int)
{
    switch (key) {
        case 'q':
        case 27:
            exit(0);
            break;
        //**********************************
        // Manage the update of Angle1 with the key 'a' and 'z'
        //**********************************
        case 'a':
            angle1 += vitesse_angle;
            break;
        case 'z':
            angle1 -= vitesse_angle;
            break;
        case 'e':
            angle2 += vitesse_angle;
            break;
        case 'r':
            angle2 -= vitesse_angle;
            break;
       case 'o':
            if (deltaPincer >= 2) {
                deltaPincer -= vitesse_pincer;
            }
            break;
        case 'l':
            if (deltaPincer <= 8) {
                deltaPincer += vitesse_pincer;
            }
            break;
        default:
            break;
    }
    glutPostRedisplay();
}


void init()
{
    glClearColor(0.f, 0.f, 0.f, 0.f);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluPerspective(65.0, 1.0, 1.0, 100.0);

    glShadeModel(GL_FLAT);
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();

    // Place the camera
    gluLookAt(4, 1, -10, .0, .0, 0., .0, 1., .0);
}


/**
 * Function called every time the main window is resized
 * @param[in] width the new window width in pixels
 * @param[in] height the new window height in pixels
 */
void reshape(int width, int height)
{

    // define the viewport transformation;
    glViewport(0, 0, width, height);
    if (width < height)
        glViewport(0, (height - width) / 2, width, width);
    else
        glViewport((width - height) / 2, 0, height, height);
}


/**
 * Function that prints out how to use the keyboard
 */
void usage()
{
    printf("\n*******\n");
    printf("Arrows key: rotate the whole robot\n");
    printf("[a][z] : move the second joint of the arm\n");
    printf("[e][r] : move the third joint of the arm\n");

    printf("[esc]  : terminate\n");
    printf("*******\n");
}


int main(int argc, char **argv) {
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB);
    glutInitWindowSize(500, 500);
    glutInitWindowPosition(100, 100);
    glutCreateWindow(argv[0]);
    init();
    glutDisplayFunc(display);

    glutReshapeFunc(reshape);
    //**********************************
    // Register the keyboard function
    //**********************************
    glutKeyboardFunc(keyboard);

    //**********************************
    // Register the special key function
    //**********************************
    glutSpecialFunc(arrows);

    // just print the help
    usage();

    glutMainLoop();

    return EXIT_SUCCESS;
}


