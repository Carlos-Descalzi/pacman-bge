//Interpolates the vertex normal across the texture fragment
varying vec3 normal;
//Interpolate the texel position in eye space.
varying vec3 ec_pos;

varying vec2 texture_coordinate;

void main()
{
	normal = gl_NormalMatrix * gl_Normal;
	ec_pos = vec3(gl_ModelViewMatrix * gl_Vertex);
	
	//Perform fixed transformation for the vertex
	gl_Position = ftransform();	
	texture_coordinate = vec2(gl_MultiTexCoord0);	
}
