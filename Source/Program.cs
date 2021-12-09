using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace AaC
{
    class Program
    {
        public const string usage = "Provide input file path. Add '-a' to use approximate algorithm. Add '-i' to skip producing output file.\n";

        private static List<int> GenerateBaseSequence(int size)
        {
            var list = new List<int>( size );
            for ( int i = 0; i < size; i++ )
                list.Add(i );
            return list;
        }

        public static List<T> Swap<T>(List<T> list, int indexA, int indexB)
        {
            T tmp = list[ indexA ];
            list[ indexA ] = list[ indexB ];
            list[ indexB ] = tmp;
            return list;
        }

        public static void CreateSequences(ref List<List<int>> sequenceList, List<int> baseSequence, int firstElement = 0)
        {
            if ( firstElement == baseSequence.Count )
                sequenceList.Add( baseSequence );
            else
            {
                for(int i = firstElement; i < baseSequence.Count; i++ )
                {
                    Swap( baseSequence, firstElement, i );
                    CreateSequences( ref sequenceList, new List<int>( baseSequence ), firstElement + 1 );
                    Swap( baseSequence, firstElement, i );
                }
            }
        }

        public static List<int> EmptyIntListOfSize(int size)
        {
            var list = new List<int>(size);
            for(int i = 0; i < size; i++ )
            {
                list.Add( -1 );
            }
            return list;
        }

        public static List<List<int>> GenerateMatrixFromSequenceCombination( List<List<int>> matrix, List<int> sequence )
        {
            int size = sequence.Count;
            var ret = new List<List<int>>( size );
            for ( int i = 0; i < size; i++ )
                ret.Add( EmptyIntListOfSize(size) );

            for(int i = 0; i < size; i++ )
            {
                for(int j = 0; j < size; j++ )
                {
                    ret[ i ][ j ] = matrix[ sequence[ i ] ][ sequence[ j ] ];
                }
            }

            return ret;
        }

        public static List<List<int>> RevertRearrangedMatrix( List<List<int>> rearangedMatrix, List<int> sequence )
        {
            int size = sequence.Count;
            var ret = new List<List<int>>( size );
            for ( int i = 0; i < size; i++ )
                ret.Add( EmptyIntListOfSize(size) );

            for ( int i = 0; i < size; i++ )
            {
                for ( int j = 0; j < size; j++ )
                {
                    ret[ sequence[ i ] ][ sequence[ j ] ] = rearangedMatrix[ i ][ j ];
                }
            }

            return ret;
        }

        public static int CalculateCommonEdges(List<List<int>> matrix, int smallerMatrixSize)
        {
            int commonEdges = 0;
            for(int i = 0; i < smallerMatrixSize; i++ )
            {
                for(int j = 0; j < smallerMatrixSize; j++ )
                {
                    if ( matrix[ i ][ j ] == 2 )
                        commonEdges++;
                }
            }
            return commonEdges;
        }

        public static List<int> GenerateSequenceOfLabelsFromMaxDegree( List<List<int>> matrix, int matrixSize )
        {
            var degrees = matrix.Select( vertex => vertex.Where( edge => edge > 0 ).Count() ).ToList();

            List<KeyValuePair<int, int>> labelWithDegree = new List<KeyValuePair<int, int>>( matrixSize );
            for ( int i = 0; i < matrixSize; i++ )
                labelWithDegree.Add( new KeyValuePair<int, int>( i, degrees[ i ] ) );

            labelWithDegree.Sort( ( kvp1, kvp2 ) => kvp2.Value.CompareTo( kvp1.Value ) );

            return labelWithDegree.Select( kvp => kvp.Key ).ToList();
        }

        public static List<int> GenerateApproximateSequence( List<List<int>> biggerMatrix, int biggerMatrixSize, List<List<int>> smallerMatrix, int smallerMatrixSize )
        {
            var sequenceBigger = GenerateSequenceOfLabelsFromMaxDegree( biggerMatrix, biggerMatrixSize );
            var sequenceSmaller = GenerateSequenceOfLabelsFromMaxDegree( smallerMatrix, smallerMatrixSize );

            var realSequence = EmptyIntListOfSize( biggerMatrixSize );

            for(int i = 0; i < sequenceSmaller.Count; i++ )
                realSequence[ sequenceSmaller[ i ] ] = sequenceBigger[ i ];

            for(int i = sequenceSmaller.Count; i < sequenceBigger.Count; i++ )
                realSequence[ i ] = sequenceBigger[ i ];

            return realSequence;
        }

        public static void ReadMatrices(string path, out List<List<int>> biggerMatrix, out int biggerMatrixSize, out List<List<int>> smallerMatrix, out int smallerMatrixSize)
        {
            string[] lines = File.ReadAllLines( path );
            int firstMatrixSize = Int32.Parse( lines[ 0 ] );
            int secondMatrixSize = Int32.Parse( lines[ firstMatrixSize + 1 ] );
            List<List<int>> firstMatrix = new List<List<int>>( firstMatrixSize );
            List<List<int>> secondMatrix = new List<List<int>>( secondMatrixSize );

            for(int i = 1; i <= firstMatrixSize; i++ )
            {
                string line = lines[ i ];
                firstMatrix.Add(line.Split( ' ' ).Select(str => Int32.Parse(str)).ToList());
            }

            for ( int i = 1; i <= secondMatrixSize; i++ )
            {
                string line = lines[ firstMatrixSize + 1 + i ];
                secondMatrix.Add(line.Split( ' ' ).Select( str => Int32.Parse( str ) ).ToList());
            }

            if(firstMatrixSize > secondMatrixSize)
            {
                biggerMatrix = firstMatrix;
                biggerMatrixSize = firstMatrixSize;
                smallerMatrix = secondMatrix;
                smallerMatrixSize = secondMatrixSize;
            }
            else
            {
                biggerMatrix = secondMatrix;
                biggerMatrixSize = secondMatrixSize;
                smallerMatrix = firstMatrix;
                smallerMatrixSize = firstMatrixSize;
            }
        }

        public static string GraphToString(List<List<int>> graph)
        {
            string res = "";
            foreach(var line in graph)
            {
                foreach(var edge in line)
                {
                    res += $"{edge} ";
                }
                res = res.Remove( res.Length - 1 );
                res += "\n";
            }
            return res.Remove( res.Length - 1 );
        }

        public static void SaveAnswer(int numberOfCommonEdges, List<int> mappingSequence, List<List<int>> graph, bool isApproximate, List<List<int>> smallerGraph, List<List<int>> biggerGraph,int biggerMatrixSize, long executionTimeInMs)
        {
            string res = "";
            res += isApproximate ? "APPROXIMATE\n\n" : "EXACT\n\n";
            res += $"Common edges:\n{numberOfCommonEdges}\n\n";
            res += $"Execution time in ms: \n{executionTimeInMs}\n\n";
            string mappingSequenceStr = "";
            foreach(var n in mappingSequence)
                mappingSequenceStr += $"{n} ";
            mappingSequenceStr = mappingSequenceStr.Remove( mappingSequenceStr.Length - 1 );
            res += $"Mapping sequence:\n{mappingSequenceStr}\n\n";
            res += $"Smaller original graph:\n{GraphToString( smallerGraph )}\n\n";
            res += $"Bigger original graph:\n{GraphToString( biggerGraph )}\n\n";
            res += $"Mapped sequence on a larger graph:\n{GraphToString( graph )}\n\n";
            res += $"Common subgraph/supergraph on larger graph:\n{GraphToString( RevertRearrangedMatrix( graph, mappingSequence ) )}";
            File.WriteAllText( "answer.txt", res );
            Console.Write(biggerMatrixSize < 26 ? res+"\n\n" : "The file was too large to print in the output. The results were saved in answer file.\n\n");
        }

        public static void Main( string[] args )
        {
            if(args.Length < 1)
            {
                Console.WriteLine( usage );
                return;
            }
            if(!File.Exists(args[0]))
            {
                Console.WriteLine("The given file does not exist!\n");
                Console.WriteLine(usage);
                return;
            }
            string inputPath = args[ 0 ];

            ReadMatrices( inputPath, out List<List<int>> biggerMatrix, out int biggerMatrixSize, out List<List<int>> smallerMatrix, out int smallerMatrixSize );

            bool approximate = args.Any( v => v == "-a" );
            bool skipOutputFile = args.Any( v => v == "-i" );

            var sequenceList = new List<List<int>>();

            var watch = new System.Diagnostics.Stopwatch();
            watch.Start();

            if(approximate)
                sequenceList.Add( GenerateApproximateSequence( biggerMatrix, biggerMatrixSize, smallerMatrix,    smallerMatrixSize ) );
            else
                CreateSequences( ref sequenceList, GenerateBaseSequence( biggerMatrixSize ) );

            var mostMatchingSequence = new List<int>();
            var smallestCommonSupergraph = new List<List<int>>();
            int mostMatchingEdges = 0;

            foreach(var sequence in sequenceList)
            {
                var rearrangedMatrix = GenerateMatrixFromSequenceCombination( biggerMatrix, sequence );
                for(int i = 0; i < smallerMatrixSize; i++ )
                {
                    for(int j = 0; j < smallerMatrixSize; j++ )
                    {
                        rearrangedMatrix[ i ][ j ] += smallerMatrix[ i ][ j ];
                    }
                }
                int commonEdges = CalculateCommonEdges( rearrangedMatrix, smallerMatrixSize );
                if (commonEdges > mostMatchingEdges)
                {
                    mostMatchingEdges = commonEdges;
                    mostMatchingSequence = sequence;
                    smallestCommonSupergraph = rearrangedMatrix;
                }
            }

            watch.Stop();
            if(!skipOutputFile && mostMatchingEdges!=0)
                SaveAnswer( mostMatchingEdges, mostMatchingSequence, smallestCommonSupergraph, approximate, smallerMatrix, biggerMatrix, biggerMatrixSize, watch.ElapsedMilliseconds );

            Console.WriteLine( $"Found common edges: {mostMatchingEdges}" );
            Console.WriteLine( $"Ellapsed time: {watch.ElapsedMilliseconds}" );
        }
    }
}
