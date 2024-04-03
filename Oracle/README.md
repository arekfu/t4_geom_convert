# Using the Oracle comparison tool

1. Create a source that encompass the geometrical area required to be tested.  
   tip for saving computation time: cut just lower the birth energy so particles are killed after one collision  
   
2. Add the ptrac card keeping only the source events.  
   Note: currently only the binary version seems to be working  
```
PTRAC FILE=BIN EVENT=SRC
```
3. Select the number of point to be tested (number of source particles)  

4. Run the mcnp calculation  
 
```mcnp6 name=<mcnp_input>.i```  
After running, a file  `<mcnp_input>.ip` should be created

5. Compare to the T4 input data 

```
/path/to/build/oracle -n 100 <t4_input>.t4 <mcnp_input>.i <mcnp_input>.ip
```
note: if you do not use the converter to generate your TRIPOLI-4 input, make sure that the naming convention of the materials is respected.  
Otherwise, the comparison will fail as this oracle compares the material at given positions.
