import JSON

function valid_moves(precept)
    grid = precept["grid"]
    moves = Int64[]
    for (i, col) in enumerate(grid)
        if col[1] == 0
            push!(moves, i)
        end
    end
    return moves
end

function main()
    println(stderr, "Connect Four in Julia")
    for json in eachline()
        println(stderr, json)
        precept = JSON.parse(json)
        moves = valid_moves(precept)
        move = rand(moves) - 1
        action = Dict("move" => move)
        action_json = JSON.json(action)
        println(stderr, action_json)
        println(action_json)
        flush(stdout)
    end
end

main()